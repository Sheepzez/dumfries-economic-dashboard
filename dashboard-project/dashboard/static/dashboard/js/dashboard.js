/*jshint*/
/*global angular, drawGraph, console, alert, prompt, add_Trend_Element, jsPDF, svgElementToPdf, d3 */
'use strict';

var app = angular.module('dashboard', ['ngRoute', 'gridster']);
var GLOBAL = {};
var drawAllGraphs = function() {
    if (!GLOBAL.widgets) return;
    for (var i = 0; i < GLOBAL.widgets.length; i++) {
        //console.log("Drawing graph: " + GLOBAL.widgets[i].id);
        drawGraph(GLOBAL.widgets[i].id, GLOBAL.widgets[i].dataset, GLOBAL.widgets[i].type,GLOBAL.widgets[i].datasetLabels);
    }
    $('[data-toggle="popover"]').popover({html: true});
};

var showPopover = function(event) {
        $(event.target).closest('[data-toggle="popover"]').popover("toggle");
    };

app.run(function($rootScope, $templateCache) {
    $rootScope.$on('$routeChangeStart', function(event, next, current) {
        if (typeof(current) !== 'undefined') {
            $templateCache.remove(current.templateUrl);
        }
    });
});

app.run(['gridsterConfig', '$rootScope', function(gridsterConfig, $rootScope) {
    gridsterConfig.resizable.stop = function(event, uiWidget, $element) {
        $rootScope.$broadcast('resize');
    };
}]);

app.config(function($routeProvider) {
    $routeProvider
    // route for the home page
        .when('/', {
        templateUrl: 'pages/home',
        controller: 'mainController'
    })

    // route for the about page
    .when('/category', {
        templateUrl: 'pages/category'
    })

    .when('/category/:category', {
        templateUrl: function(params) {
            return 'pages/category/' + params.category;
        },
        controller: 'categoryController'
    })

    .when('/savedconfigs', {
        templateUrl: 'pages/savedConfigs'
    })
    
    .when('/search/:searchTerm', {
        templateUrl: function(params) {
            return 'pages/searchResult/' + params.searchTerm;
        },
        controller: 'searchController'
    })

    .when('/register', {
        templateUrl: 'pages/register'
    });
});

// create the controller and inject Angular's $scope
app.controller('mainController', function($scope, $location, $timeout) {
    $scope.widgets = GLOBAL.widgets;

    $scope.saveConfig = function() {
        var widgets = GLOBAL.widgets,
            data = [];
        $.ajax({
            type: "GET",
            url: '/account/checkAuthenticated',
            success: function(response) {
                if (!response.is_authenticated) {
                    alert("Please log in first.");
                    return;
                }
                var name = prompt("Enter a name for the config: ");
                if (!name) return;
                for (var i = 0; i < widgets.length; i++) {
                    var object = {};
                    object.visPK = widgets[i].pk;
                    object.xPosition = widgets[i].col;
                    object.yPosition = widgets[i].row;
                    object.sizeX = widgets[i].sizeX;
                    object.sizeY = widgets[i].sizeY;
                    data.push(object);
                }
                console.log(data);
                $.ajax({
                    type: "POST",
                    url: '/saveConfig',
                    data: {
                        data: JSON.stringify(data),
                        name: name
                    },
                    success: function(response) {
                        alert(response.message);
                    },
                    error: function(err) {
                        console.log(err);
                    }
                });
            }
        });
    };
    
    $scope.clear = function() {
        if (!$scope.widgets) $scope.widgets = GLOBAL.widgets;
        console.log($scope.widgets);
        $scope.widgets.splice(0, $scope.widgets.length);
    };
    
    $("#searchForm").submit(function(event) {
        
        /* stop form from submitting normally */
        event.preventDefault();
        event.stopImmediatePropagation();

        /* get some values from elements on the page: */
        var $form = $(this),
            searchVal = $form.find("#srch-term").val();
        
        $location.path("/search/" + searchVal).replace();
        $scope.$apply();
        console.log($location);
        return false;
    });
    
    $(".addGraph").on("click", function(e) {
        console.log(e);
        console.log(this);
        var $this = $(this);
        
        if ($this.parent().hasClass("disabled")) return;
        
        var id = $this.attr("data-pk");
        
        $.ajax({
            type: "GET",
            url: "/getGraph",
            data: {
                id: id
            },
            success: function(widget) {
                console.log(widget);
                GLOBAL.widgets.push(widget);
                $scope.$apply();
                $timeout(drawAllGraphs, 500);
            },
            error: function(err) {
                console.log(err);
            }
        });
    });

});

app.controller('savedConfigController', function($scope, $route) {
    $scope.deleteSavedConfig = function(id) {
        $.ajax({
            type: "POST",
            url: '/deleteSavedConfig',
            data: {
                id: id
            },
            success: function(response) {
                if (response.success)
                    $route.reload();
                else
                    alert(response.message);
            },
            error: function(err) {
                console.log(err);
            }
        });
    };

    $scope.loadSavedConfig = function(id) {
        $.ajax({
            type: "POST",
            url: '/loadSavedConfig',
            data: {
                id: id
            },
            success: function(response) {
                console.log(response);
                GLOBAL.widgets = response.widgets;
                var el = $("#config" + id);
                console.log(el);
                el.removeClass("glyphicon-import");
                el.addClass("glyphicon-saved");
                el.addClass("icon-success");
                setTimeout(function() {
                    el.removeClass("glyphicon-saved");
                    el.removeClass("icon-success");
                    el.addClass("glyphicon-import");
                }, 1000);
            },
            error: function(err) {
                console.log(err);
            }
        });
    };
});

app.controller('draggableGridController', function($scope, $timeout) {
    $scope.gridsterOptions = {
        margins: [20, 20],
        columns: 6,
        pushing: true,
        outerMargin: false,
        draggable: {
            enabled: true,
            start: function(event, $element, widget) {},
            stop: function(event, $element, widget) {}
        },
        resizable: {
            enabled: true,
            handles: ['n', 'e', 's', 'w', 'ne', 'se', 'sw', 'nw'],
            start: function(event, $element, widget) {},
            resize: function(event, $element, widget) {},
            stop: function(event, $element, widget) {
                $timeout(drawAllGraphs, 500);
		        console.log("REDRAWING GRAPHS");
            }
        },
        minSizeX: 2,
        minSizeY: 1,
        swapping: true, // whether or not to have items of the same size switch places instead of pushing down if they are the same size
        width: 'auto', // can be an integer or 'auto'. 'auto' scales gridster to be the full width of its containing element
        colWidth: 'auto', // can be an integer or 'auto'.  'auto' uses the pixel width of the element divided by 'columns'
        rowHeight: 'match',
        floating: true
    };

    $scope.$on('gridster-resized', function(sizes, gridster) {
        $timeout(drawAllGraphs, 500);
    });

    $scope.widgets = GLOBAL.widgets;
    $scope.deleteWidget = function(index) {
        $scope.widgets.splice(index, 1);
    };
    
    $scope.showPopover = showPopover;
    
    $scope.exportToPDF = function() {
        var maxCol = -1, maxRow = -1, maxColSize = -1, maxRowSize = -1;

        for (var i=0; i<GLOBAL.widgets.length; i++) {
            var widget = GLOBAL.widgets[i],
                $vis = $("#" + widget.id),
                width = $vis.parent().width(),
                height = $vis.parent().height();
            console.log(widget);
            if (widget.row > maxRow) {
                maxRow = widget.row;
            }
            
            if (widget.col > maxCol) {
                maxCol = widget.col;
            }
            
            if (width > maxColSize) {
                maxColSize = width;
            }
            
            if (height > maxRowSize) {
                maxRowSize = height;
            }
        }
        
        var doc = new jsPDF("portrait", "pt", "a4");
        var image = new Image();

        // create an empty canvas element
        var canvas = document.createElement("canvas"),
            canvasContext = canvas.getContext("2d");

        // Called when image has finished loading.
        image.onload = function () {
            //Set canvas size is same as the picture
            canvas.width = image.width;
            canvas.height = image.height;
     
            // draw image into canvas element
            canvasContext.drawImage(image, 0, 0, image.naturalWidth, image.naturalHeight);
     
            // get canvas contents as a data URL (returns png format by default)
            var dataURL = canvas.toDataURL();
            
            // currHeight records how far down we are through this page.
            var currHeight = 0;
            
            // How wide the image will be in the PDF
            var newWidth = 500;
            doc.addImage(dataURL, 'PNG', 40, 20, newWidth, newWidth * (image.naturalHeight / image.naturalWidth));
            currHeight += 20 + newWidth * (image.naturalHeight / image.naturalWidth);
            
            currHeight += 50;
            doc.setFontSize(22);
            doc.text(150, currHeight, "Generated by Crichton Institute's");
            currHeight += 25;
            
            doc.text(140, currHeight, "Dumfries and Galloway Dashboard");
            currHeight += 30;
            
            doc.setFontSize(20);
            doc.text(180, currHeight, 'Created on ' + (new Date()).toDateString() + ".");
            currHeight += 30;
            
            doc.setFontSize(16);
            doc.addPage(maxCol * maxColSize, maxRow * maxRowSize);
            
            var svgCount = 0;
            $("svg.chart").each(function(index, element) {
                var $element = $(element),
                    widget = GLOBAL.widgets[index];
                svgCount++;
                    
                function addImage(blob, image) {
                    doc.addImage(blob, 'PNG', image.naturalWidth * widget.col / widget.sizeX + 20, image.naturalHeight * widget.row / widget.sizeY + 20, image.naturalWidth, image.naturalHeight);
                    
                    if (--svgCount === 0) {
                        doc.save('Dumfries-Galloway Dashboard Export.pdf');
                    }
                }
                
                element.toDataURL("image/png", {
                    callback: function(data) {
                        var i = new Image(); 
                        i.onload = function() {
                            addImage(data, i);
                        };
                        i.src = data; 
                    }
                });
            });
        };
        
        // Sets src and starts loading. image.onLoad will be called when image is loaded.
        image.src = $("#banner").attr('src');
    };

    if (!GLOBAL.widgets) {
        $.ajax({
            type: "GET",
            url: '/getGraphs',
            success: function(response) {
                GLOBAL.widgets = response.widgets;
                $scope.widgets = GLOBAL.widgets;
                $timeout(drawAllGraphs, 1000); // TODO - fix this hacky solution to randomly wait 500ms before drawing graphs. 
                $scope.$watch("widgets", function(newValue, oldValue) {
                    $(".addGraph").each(function(index, element) {
                        var found = false;
                        for(var i=0; i < newValue.length; i++) {
                            if (parseInt($(element).attr("data-pk"), 10) === newValue[i].pk) {
                                $(element).parent().addClass("disabled");
                                found = true;
                                break;
                            }
                        }
                        if (!found) {
                            $(element).parent().removeClass("disabled");
                        }
                    });
                    
                }, true);
            },
            error: function(err) {
                console.log(err);
            }
        });
    } else {
        $timeout(drawAllGraphs, 500); // TODO - Also fix this hacky solution
    }

});


app.controller('categoryController', function($scope, $timeout) {
    var drawCategoryGraphs = function() {
        for (var i=0; i<GLOBAL.currentCategoryWidgets.length; i++) {
            var widget = GLOBAL.currentCategoryWidgets[i];
            drawGraph("graph" + widget.pk, widget.dataset, widget.type);
            //add_Trend_Element("graph" + widget.pk);
        }
    };
	$('.daterange').on('apply.daterangepicker', function(ev, picker) {
	  drawCategoryGraphs();
	});
    drawCategoryGraphs();
});

app.controller("searchController", function($scope) {
    var drawSearchGraphs = function() {
        for (var i=0; i<GLOBAL.currentSearchWidgets.length; i++) {
            var widget = GLOBAL.currentSearchWidgets[i];
            drawGraph("graph" + widget.pk, widget.dataset, widget.type);
        }
    };
    $('[data-toggle="popover"]').popover({html: true});
    $scope.showPopover = showPopover;
    drawSearchGraphs();
});



function logoutUser() {
    $.ajax({
        type: "POST",
        url: '/account/login',
        data: $('#login_form').serialize(),
        success: function(response) {
            $("#message").html();
        }
    });
}

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});
