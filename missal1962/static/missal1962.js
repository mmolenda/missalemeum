

$(document).ready(function()    {

    // making :contains case insensitive
    $.expr[":"].contains = $.expr.createPseudo(function(arg) {
        return function( elem ) {
            return $(elem).text().toUpperCase().indexOf(arg.toUpperCase()) >= 0;
        };
    });

    moment.locale("pl");

    $('#sidebarCollapse').on('click', function () {
        $('#sidebar, #content').toggleClass('active');
    });

    $('#datetimepicker4').datetimepicker({
        format: 'YYYY-MM-DD',
        useCurrent: false,
        locale: 'pl',
        widgetPositioning: {
            horizontal: 'right',
            vertical: 'bottom'
        }
    });

    $('#datetimepicker4 input').on('input', function () {
        document.location.hash = this.value;
        $('input#search-input').val("").trigger("input");
    });

    $('#search-clear').on('click', function () {
        $('input#search-input').val("").trigger("input");
    });

    $('input#search-input').on('input', function () {
        let searchString = $(this).val();
        if (searchString === '') {
            let itemsAll = $('.sidebar-calendar-item');
            itemsAll.show();
        } else {
            if (searchString.length > 2) {
                let itemsAll = $('.sidebar-calendar-item');
                itemsAll.hide();
                $('li.sidebar-calendar-item div:contains("' + searchString + '")').parent().parent().show("fast");
            }
        }
        togglePropersSidebarItem(activeDate);
    });

    function togglePropersSidebarItem(date) {
        function markItemActive(date) {
            $("nav#sidebar li.sidebar-calendar-item").removeClass("active");
            let newActive = $("li#sidebar-calendar-item-" + date);
            newActive.addClass("active");
            let sidebar = $('nav#sidebar');

            let itemPosition = newActive.position().top;
            let sidebarPosition = Math.abs(sidebar.find('ul').position().top);

            if (Math.abs(itemPosition) > sidebar.height() * 0.6) {
                sidebar.animate({scrollTop: sidebarPosition + itemPosition - 100}, 200);
            }
        }

        let newActive = $("li#sidebar-calendar-item-" + date);
        if (newActive.length == 0) {
            loadPropersSidebar(date, markItemActive);
        } else {
            markItemActive(date);
        }
    }

    function loadProperByDate(date) {
        $.getJSON( dateEndpoint + date, function( data ) {
            let title = data['info'].title;
            let descritpion = data['info'].description;
            let sectionsVernacular = data.proper_vernacular;
            let sectionsLatin = data.proper_latin;
            let additional_info = [data['info'].date];
            if (data['info'].tempora != null) {
                additional_info.push(data['info'].tempora);
            }
            if (data['info'].additional_info != null) {
                $.merge(additional_info, data['info'].additional_info);
            }

            let main = $("main");
            main.empty();
            window.scrollTo(0, 0);

            if (title == null) {
                title = moment(data['info'].date, "YYYY-MM-DD").format("DD MMMM");
            }
            let intro = "<h1 class=\"display-8\">" + title + "</h1><p><em class=\"rubric\"'>";
            intro += additional_info.join("</em> | <em class=\"rubric\">");
            intro += "</em></p><p>" + descritpion +  "</p>";
            $(intro).appendTo(main);

            $.each([sectionsVernacular, sectionsLatin], function(i, sections) {
                $.each(sections, function(x, y) {sections[x].body = y.body.replace(/\*([^\*]+)\*/g, "<em>$1</em>")})

            });
            for (let i = 0; i < sectionsVernacular.length; i++) {
                let row = "<div class=\"row\"><div class=\"col-sm-6 section-vernacular\"><h2>" + sectionsVernacular[i].label +
                    "</h2><p>"+ sectionsVernacular[i].body.split("\n").join("<br />") +"</p></div><div class=\"col-sm-6 section-latin\"><h2>" + sectionsLatin[i].label +
                    "</h2><p>"+ sectionsLatin[i].body.split("\n").join("<br />") +"</p></div></div>";
                $(row).appendTo(main);
            }
            togglePropersSidebarItem(date);
            $('#datetimepicker4').datetimepicker("date", date);
        });
    }

    function loadPropersSidebar(date, markItemActiveCallback) {
        let year = date.split('-')[0];
        $.getJSON( calendarEndpoint + year, function( data ) {
            let sidebar = $('nav#sidebar>ul');
            sidebar.empty();

            let prevYear = parseInt(year) - 1;
            let prevYearLastDay = prevYear + '-12-31';
            $("<li class=\"sidebar-calendar-item\"><a href=\"#" + prevYearLastDay +
                "\"><div class=\"tempora rubric\">" + prevYear + " ⬏</div></a></li>").appendTo(sidebar);

            $.each(data, function(date, day) {
                let additional_info = [date];
                let celebration;
                if (day.celebration.length > 0) {
                    celebration = day.celebration[0].title;
                } else {
                    celebration = moment(date, "YYYY-MM-DD").format("DD MMMM");
                }
                if (day.tempora.length > 0 && day.tempora[0].title != celebration) {
                    additional_info.push(day.tempora[0].title);
                }

                let row = "<li id=\"sidebar-calendar-item-" + date + "\"" + " class=\"sidebar-calendar-item\"><a href=\"#" + date +
                    "\"><div>" + celebration + "</div><div class=\"tempora rubric\">" + additional_info.join(" | ") +  "</div></a></li>"
                $(row).appendTo(sidebar);


            });

            let nextYear = parseInt(year) + 1;
            let nextYearFirstDay = nextYear + '-01-01';
            $("<li class=\"sidebar-calendar-item\"><a href=\"#" + nextYearFirstDay +
                "\"><div class=\"tempora rubric\">" + nextYear + " ⬎</div></a></li>").appendTo(sidebar);

            markItemActiveCallback(date);
            $('input#search-input').attr("placeholder", "Szukaj w " + year + "...");
        });
    }

    $('input[type=radio][name=lang-switch]').change(function() {
        if (this.id == 'lang-switch-vernacular') {
            $('div.section-vernacular').show();
            $('div.section-latin').hide();
        } else {
            $('div.section-vernacular').hide();
            $('div.section-latin').show();
        }
    });

    function toggleLanguageColumns() {
        if ($(window).width() >= 576) {
            $('div.section-vernacular').show();
            $('div.section-latin').show();
        } else {
            let langId = $('#lang-switch>label.active>input').attr("id");
            if (langId == 'lang-switch-vernacular') {
                $('div.section-vernacular').show();
                $('div.section-latin').hide();
            } else {
                $('div.section-vernacular').hide();
                $('div.section-latin').show();
            }
        }
    }


    $(window).on('resize', function(){
        toggleLanguageColumns();
    });

    $(window).on('hashchange', function() {
        activeDate = document.location.hash.replace("#", "");
        loadProperByDate(activeDate);
    });

    let tmpDate = document.location.hash.replace("#", "");
    if (tmpDate == '') {
        tmpDate = moment();

    } else {
        tmpDate = moment(tmpDate, "YYYY-MM-DD");
    }
    let activeDate = tmpDate.format("YYYY-MM-DD");
    loadProperByDate(activeDate);
    toggleLanguageColumns();
});
