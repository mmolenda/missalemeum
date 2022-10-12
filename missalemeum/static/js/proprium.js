

$window.on("load", function () {

    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/service-worker.js');
    }

    /**
     *
     * Globals
     *
    **/

    // Localized strings

    const $sidebarAndContent = $("#sidebar, #content");
    const $datetimepicker4 = $("#datetimepicker4");

    const $sidebarUl = $sidebar.find("ul");

    let ploaderByDate = new ProperContentLoader(config.dateEndpoint, config.lang, function() {
        markSidebarItemActiveWithReload(getResourceId());
        $datetimepicker4.datetimepicker("date", getResourceId());
    });

    let ploaderById = new ProperContentLoader(config.properEndpoint, config.lang, function() {
        loadSidebar(moment().format("YYYY-MM-DD"), function() {});
        $sidebar.find("li.sidebar-item").removeClass("active");
    });

    function loadProper(resourceId, isHistoryReplace) {
        if (moment(resourceId, "YYYY-MM-DD", true).isValid()) {
            ploaderByDate.load(resourceId, isHistoryReplace);
        } else {
            ploaderById.load(resourceId, isHistoryReplace);
        }

    }

    function init() {
        moment.locale(config.lang);
        loadProper(getResourceId(), false);
    }

    init();

    /**
     *
     * Functions
     *
     **/

    function getResourceId() {
        if (selectedResource === undefined) {
            let url = window.location.href.replace(/#.*/, "").replace(/\?.*/, "");
            selectedResource = url.split('/').reverse()[0];
        }
        if (selectedResource === "" || selectedResource === config.lang) {
            return moment().format("YYYY-MM-DD");
        }
        let tmpDate = moment(selectedResource, "YYYY-MM-DD", true);
        if (tmpDate.isValid()) {
            return tmpDate.format("YYYY-MM-DD");
        } else {
            return selectedResource;
        }
    }

    /**
      * Obtain calendar for the year specified in `date` through AJAX call and populate
      * the sidebar with <li> elements.
      * Once populated, fire the callback function to activate selected item and clear the search input.
     **/
    function loadSidebar(date, markItemActiveCallback) {
        loader.show();
        let year = date.split("-")[0];
        let prevYear = parseInt(year) - 1;
        let prevYearLastDay = prevYear + "-12-31";
        let nextYear = parseInt(year) + 1;
        let nextYearFirstDay = nextYear + "-01-01";
        $.getJSON( config.calendarEndpoint + year, function( data ) {
            $sidebarUl.empty();

            if (prevYearLastDay >= $datetimepicker4.datetimepicker("minDate")._i) {
                $(renderTemplate($templateSidebarCalendarItemYear, {
                    date: prevYearLastDay,
                    year: prevYear
                })).appendTo($sidebarUl);
            }

            $.each(data, function(date, day) {
                let parsedDate = moment(date, "YYYY-MM-DD");
                let additional_info = [parsedDate.format("dd DD.MM.YYYY")];
                let celebration;
                let color;
                if (day.celebration.length > 0) {
                    celebration = day.celebration[0].title;
                    color = day.celebration[0].colors[0];
                } else {
                    celebration = "Feria";
                    color = 'w';
                    if (day.tempora.length > 0) {
                        color = day.tempora[0].colors[0];
                    }
                }
                if (day.tempora.length > 0 && day.tempora[0].title != celebration) {
                    additional_info.push(day.tempora[0].title);
                }

                let sidebarCalendarItem = $(renderTemplate($templateSidebarCalendarItem, {
                    date: date,
                    celebration: celebration,
                    additional_info: additional_info.join(" | "),
                    color: color
                }));
                if (parsedDate.weekday() === config.saturday) {
                    sidebarCalendarItem.addClass("saturday");
                }
                sidebarCalendarItem.appendTo($sidebarUl);
            });

            if (nextYearFirstDay <= $datetimepicker4.datetimepicker("maxDate")._i) {
                $(renderTemplate($templateSidebarCalendarItemYear, {
                    date: nextYearFirstDay,
                    year: nextYear
                })).appendTo($sidebarUl);
            }
        }).done(function() {
            markItemActiveCallback(date);
            $searchInput.attr("placeholder", config.translation.searchIn + year + "...");
        }).fail(function() {
            alert(config.translation.cannotLoadMessage);
        }).always(function() {
            loader.hide();
        });
    }



    /**
      * Mark sidebar element for given `date` as active. If an element is not present, reload the sidebar
      * with the data for proper year.
     **/
    function markSidebarItemActiveWithReload(date) {
        let newActive = $("li#sidebar-item-" + date);
        if (newActive.length === 0) {
            loadSidebar(date, markSidebarItemActive);
        } else {
            markSidebarItemActive(date);
        }
    }

    /**
      *
      * Bindings
      *
     **/

    $window.on("resize", function(){
        adaptSectionColumns();
    });


    $datetimepicker4.datetimepicker({
        format: "YYYY-MM-DD",
        minDate: config.minDate,
        maxDate: config.maxDate,
        useCurrent: false,
        locale: config.lang,
        widgetPositioning: {
            horizontal: "right",
            vertical: "bottom"
        }
    });

    /**
     * When the date is selected from datepicker update current date and clear the search input
     **/
    $datetimepicker4.find("input").on("input", function () {
        setResourceId(this.value);
        loadProper(getResourceId(), false);
        if ($searchInput.val() !== "") {
            $searchInput.val("").trigger("input");
        }
    });

    $(document).on('click', '#sidebar ul li a' , function(event) {
        event.preventDefault();
        setResourceId(event.currentTarget.href.split("/").pop());
        loadProper(getResourceId(), false);
    });

    window.onpopstate = function(event){
        setResourceId(event.target.location.href.split('/').reverse()[0]);
        loadProper(getResourceId(), true);
    };

    /**
     * filter out the elements in the sidebar;
     * start filtering from 3 characters on;
     * show all elements on empty input
     **/
    $searchInput.on("input", function () {
        filterSidebarItems($(this).val(), function() {markSidebarItemActiveWithReload(getResourceId())});
    });

    /**
     * X button in the search input clears current search
     **/
    //
    $("#search-clear").on("click", function () {
        $searchInput.val("").trigger("input");
    });

    /**
     * Switch between lang versions on small screens, where the switch is visible
     **/
    $("input[type=radio][name=lang-switch]").change(function() {
        toggleLangSections(this.id);
    });

    $("#print").on("click", function () {
        printContent($templateContentPrint, $loadedContent.html());
    });

    $("#copy-url").on("click", function () {
        copyURLToClipboard();
    });
});
