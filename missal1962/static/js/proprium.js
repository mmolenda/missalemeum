

$(window).on("load", function () {

    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/service-worker.js');
    }

    /**
     *
     * Globals
     *
    **/

    const $templateSidebarCalendarItem = $("#template-sidebar-item").text();
    const $templateSidebarCalendarItemYear = $("#template-sidebar-item-year").text();
    const $templateContentIntro = $("#template-content-intro").text();
    const $templateContentSupplementList = $("#template-content-supplement-list").text();
    const $templateContentSupplementItemInternal = $("#template-content-supplement-item-internal").text();
    const $templateContentSupplementItemExternal = $("#template-content-supplement-item-external").text();
    const $templateContentColumns = $("#template-content-columns").text();
    const $templateContentPrint = $("#template-content-print").text();

    const $window = $(window);
    const $sidebarAndContent = $("#sidebar, #content");
    const $datetimepicker4 = $("#datetimepicker4");
    const $searchInput = $("input#search-input");
    const $sidebarUl = $sidebar.find("ul");

    let loadedProperDate;
    let selectedDate;

    function init() {
        moment.locale("pl");
        loadProper(getDate());
    }

    init();

    /**
     *
     * Functions
     *
     **/

    function getDate() {
        if (selectedDate === undefined) {
            let url = window.location.href.replace(/#.*/, "");
            selectedDate = url.split('/').reverse()[0];
        }
        let tmpDate = moment(selectedDate, "YYYY-MM-DD");
        if (! tmpDate.isValid()) {
            tmpDate = moment();
        }
        return tmpDate.format("YYYY-MM-DD");
    }

    function setDate(date) {
        selectedDate = date;
    }

    /**
      * Obtain calendar for the year specified in `date` through AJAX call and populate
      * the sidebar with <li> elements.
      * Once populated, fire the callback function to activate selected item and clear the search input.
     **/
    function loadSidebar(date, markItemActiveCallback) {
        showLoader();
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
                let additional_info = [date];
                let celebration;
                if (day.celebration.length > 0) {
                    celebration = day.celebration[0].title;
                } else {
                    celebration = parsedDate.format("DD MMMM");
                }
                if (day.tempora.length > 0 && day.tempora[0].title != celebration) {
                    additional_info.push(day.tempora[0].title);
                }

                let sidebarCalendarItem = $(renderTemplate($templateSidebarCalendarItem, {
                    date: date,
                    celebration: celebration,
                    additional_info: additional_info.join(" | ")
                }));
                if (parsedDate.weekday() === 5) {
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
            $searchInput.attr("placeholder", "Szukaj w " + year + "...");
        }).fail(function() {
            alert(cannotLoadMessage);
        }).always(function() {
            hideLoader();
        });
    }

    /**
      * Obtain a proper for the given `date` through AJAX call and populate
      * the main element with Bootstrap grid.
      * Once populated, mark corresponding element in the sidebar as active and select given date in the datepicker.
     **/
    function loadProper(date, historyReplace = false) {
        if (loadedProperDate === getDate()) {
            return;
        }
        showLoader();
        let titles = [];
        $.getJSON(config.dateEndpoint + date, function(data) {
            $loadedContent.empty();
            window.scrollTo(0, 0);

            $.each(data, function(index, item) {
                let info = item["info"];
                let date = info.date;
                let title = info.title;
                let description = info.description;
                let supplements = info.supplements;
                let sectionsVernacular = item.proper_vernacular;
                let sectionsLatin = item.proper_latin;
                let additional_info = [date, mapRank(info.rank)];
                if (info.tempora != null) {
                    additional_info.push(info.tempora);
                }
                if (info.additional_info != null) {
                    $.merge(additional_info, info.additional_info);
                }

                if (title == null) {
                    title = moment(date, "YYYY-MM-DD").format("DD MMMM");
                }
                titles.push(title);
                $(renderTemplate($templateContentIntro, {
                    title: title,
                    additional_info: additional_info.join('</em> | <em class="rubric">'),
                    description: description.split("\n").join("<br />")
                })).appendTo($loadedContent);

                if (supplements.length > 0) {
                    let supplementsList = $(renderTemplate($templateContentSupplementList, {}));
                    $.each(supplements, function(index, supplement) {
                        let template;
                        if (supplement.path, supplement.path.valueOf().startsWith("http")) {
                            template = $templateContentSupplementItemExternal;
                        } else {
                            template = $templateContentSupplementItemInternal;
                        }
                        $(renderTemplate(template, {
                            path: supplement.path,
                            label: supplement.label,
                            date: date
                        })).appendTo(supplementsList);
                        if (index + 1 < supplements.length) {
                            supplementsList.append(",&nbsp;&nbsp;");
                        }
                    });
                    supplementsList.appendTo($loadedContent);
                }

                $.each([sectionsVernacular, sectionsLatin], function(i, sections) {
                    // replacing all surrounding asterisks with surrounding <em>s in body
                    $.each(sections, function(x, y) {sections[x].body = y.body.replace(/\*([^\*]+)\*/g, "<em>$1</em>")})

                });
                for (let i = 0; i < sectionsVernacular.length; i++) {
                    let sectionVernacular = sectionsVernacular[i];
                    let sectionLatin = sectionsLatin[i];
                    if (sectionLatin == null) {
                        sectionLatin = {label: "", body: ""};
                        console.error("Latin sections missing in " + date);
                    }
                    $(renderTemplate($templateContentColumns, {
                        labelVernacular: sectionVernacular.label,
                        sectionVernacular: sectionVernacular.body.split("\n").join("<br />"),
                        labelLatin: sectionLatin.label,
                        sectionLatin: sectionLatin.body.split("\n").join("<br />")
                    })).appendTo($loadedContent);
                }
            });
        }).done(function() {
            loadedProperDate = date;
            if (historyReplace === true) {
                window.history.replaceState({date: date}, '', '/' + date);
            } else {
                window.history.pushState({date: date}, '', '/' + date);
            }
            document.title = titles[0] + " | " + date + " | " + "Mszał Rzymski";
            markSidebarItemActiveWithReload(date);
            $datetimepicker4.datetimepicker("date", date);
            if (navbarIsCollapsed()) {
                $sidebarAndContent.removeClass("active");
            }
            adaptSectionColumns();
        }).fail(function() {
            alert(cannotLoadMessage);
        }).always(function() {
            hideLoader();
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

    function mapRank(rank) {
        return {1: '1 klasy', 2: '2 klasy', 3: '3 klasy', 4: '4 klasy'}[rank]
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
        locale: "pl",
        widgetPositioning: {
            horizontal: "right",
            vertical: "bottom"
        }
    });

    /**
     * When the date is selected from datepicker update current date and clear the search input
     **/
    $datetimepicker4.find("input").on("input", function () {
        setDate(this.value);
        loadProper(getDate());
        if ($searchInput.val() !== "") {
            $searchInput.val("").trigger("input");
        }
    });

    $(document).on('click', '#sidebar ul li a' , function(event) {
        event.preventDefault();
        setDate(event.currentTarget.href.split("/").pop());
        loadProper(getDate());
    });

    window.onpopstate = function(event){
        setDate(event.target.location.href.split('/').reverse()[0]);
        loadProper(getDate(), true);
    };

    /**
     * filter out the elements in the sidebar;
     * start filtering from 3 characters on;
     * show all elements on empty input
     **/
    $searchInput.on("input", function () {
        filterSidebarItems($(this).val(), function() {markSidebarItemActiveWithReload(getDate())});
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
});
