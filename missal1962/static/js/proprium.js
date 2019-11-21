

$(window).on("load", function () {

    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/service-worker.js');
    }

    /**
     *
     * Globals
     *
    **/

    // Making :contains case insensitive
    $.expr[":"].contains = $.expr.createPseudo(function(arg) {
        return function( elem ) {
            return $(elem).text().toUpperCase().indexOf(arg.toUpperCase()) >= 0;
        };
    });

    const $templateSidebarCalendarItem = $("#template-sidebar-calendar-item").text();
    const $templateSidebarCalendarItemYear = $("#template-sidebar-calendar-item-year").text();
    const $templateContentIntro = $("#template-content-intro").text();
    const $templateContentSupplement = $("#template-content-supplement").text();
    const $templateContentColumns = $("#template-content-columns").text();
    const $templateContentPrint = $("#template-content-print").text();

    const $window = $(window);
    const $sidebar = $("nav#sidebar");
    const $main = $("main");
    const $sidebarAndContent = $("#sidebar, #content");
    const $datetimepicker4 = $("#datetimepicker4");
    const $searchInput = $("input#search-input");
    const $sidebarUl = $sidebar.find("ul");
    const $sidebarTools = $("div#sidebar-tools");

    let loadedProperDate;
    let selectedDate;
    let cannotLoadMessage = "Nie udało się pobrać danych.";

    let supplementsMap = {
        "tempora:Adv1-0:1": {title: "Adwent", id: "2-adwent"},
        "sancti:12-24:1": {title: "Boże Narodzenie", id: "3-boze-narodzenie"},
        "tempora:Epi1-0:2": {title: "Okres po Objawieniu", id: "4-okres-po-objawieniu"},
        "tempora:Quadp1-0:2": {title: "Przedpoście", id: "5-przedposcie"},
        "tempora:Quadp3-3:1": {title: "Wielki Post", id: "6-wielki-post"},
        "tempora:Quad5-0:1": {title: "Okres Męki Pańskiej", id: "7-okres-meki-panskiej"},
        "tempora:Quad6-0r:1": {title: "Wielki Tydzień", id: "8-wielki-tydzien"},
        "tempora:Quad6-6r:1": {title: "Okres-Wielkanocny", id: "9-okres-wielkanocny"},
        "tempora:Pasc6-6:1": {title: "Zesłanie Ducha św.", id: "10-zeslanie-ducha-sw"},
        "tempora:Pent01-0r:1": {title: "Okres po Zesłaniu Ducha św.", id: "10-okres-po-zeslaniu-ducha-sw"}
    };

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
            $main.empty();
            window.scrollTo(0, 0);

            $.each(data, function(index, item) {
                let date = item["info"].date;
                let id = item["info"].id;
                let title = item["info"].title;
                let description = item["info"].description;
                let sectionsVernacular = item.proper_vernacular;
                let sectionsLatin = item.proper_latin;
                let additional_info = [date, mapRank(item["info"].rank)];
                if (item["info"].tempora != null) {
                    additional_info.push(item["info"].tempora);
                }
                if (item["info"].additional_info != null) {
                    $.merge(additional_info, item["info"].additional_info);
                }

                if (title == null) {
                    title = moment(date, "YYYY-MM-DD").format("DD MMMM");
                }
                titles.push(title);
                $(renderTemplate($templateContentIntro, {
                    title: title,
                    additional_info: additional_info.join('</em> | <em class="rubric">'),
                    description: description.split("\n").join("<br />")
                })).appendTo($main);

                let supplement = supplementsMap[id];
                if (supplement !== undefined) {
                    $(renderTemplate($templateContentSupplement, {
                        supplement_id: supplement.id,
                        supplement_title: supplement.title,
                        date: date
                    })).appendTo($main);
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
                    })).appendTo($main);
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
            toggleSidebarItem(date);
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
    function toggleSidebarItem(date) {
        function markItemActive(date) {
            $sidebar.find("li.sidebar-calendar-item").removeClass("active");
            let newActive = $("li#sidebar-calendar-item-" + date);
            newActive.addClass("active");

            let itemPosition = newActive.position().top;
            let sidebarPosition = Math.abs($sidebar.find("ul").position().top);

            if ((itemPosition > $sidebar.height() * 0.6) || itemPosition < $sidebarTools.height() * 1.5) {
                $sidebar.animate({scrollTop: sidebarPosition + itemPosition - 100}, 200);
            }
        }

        let newActive = $("li#sidebar-calendar-item-" + date);
        if (newActive.length == 0) {
            loadSidebar(date, markItemActive);
        } else {
            markItemActive(date);
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
        setDate(event.currentTarget.href.split("#").pop());
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
        let searchString = $(this).val();
        if (searchString === "") {
            let itemsAll = $sidebar.find("li.sidebar-calendar-item");
            itemsAll.show();
            toggleSidebarItem(getDate());
        } else if (searchString.length > 2) {
            let itemsAll = $sidebar.find("li.sidebar-calendar-item");
            itemsAll.hide();
            $('li.sidebar-calendar-item div:contains("' + searchString + '")').parent().parent().show("fast");
        }
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
        let newWindow = window.open('','', "width=650, height=750");
        let newContent = renderTemplate($templateContentPrint, {main: $main.html()});
        newWindow.document.write(newContent);
        newWindow.document.close();
        newWindow.focus();
        return true;
    });
});
