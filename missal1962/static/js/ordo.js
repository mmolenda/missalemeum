$(window).on("load", function () {

    const templateSectionTitle = $("#template-section-title").text();
    const templateOrdoItem = $("#template-ordo-item").text();
    const templateSectionSubTitle = $("#template-section-subtitle").text();
    const templateRubric = $("#template-rubric").text();
    const templateContentColumns = $("#template-content-columns").text();
    const templateSidebarItem = $("#template-sidebar-ordo-item").text();
    const templateContentPrint = $("#template-content-print").text();

    const $sidebar = $("nav#sidebar");
    let scrollTimer;

    loadOrdo();

    function loadOrdo() {
        showLoader();
        $.getJSON(config.ordoEndpoint, function( data ) {
            let $main = $("main");
            $main.empty();
            let sidebarUl = $("nav#sidebar>ul");
            sidebarUl.empty();
            window.scrollTo(0, 0);
            $(renderTemplate(templateSectionTitle, {})).appendTo($main);
            $.each(data, function(ii, item) {
                let $sidebarItem = $(renderTemplate(templateSidebarItem, {id: ii, title: item.title}));
                if (ii === 0) {
                    $sidebarItem.addClass("active");
                }
                $sidebarItem.appendTo(sidebarUl);
                let $ordoItem = $(renderTemplate(templateOrdoItem, {id: ii}));
                $(renderTemplate(templateSectionSubTitle, {title: item.title})).appendTo($ordoItem);
                $.each(item.body, function(jj, bodyItem) {
                    if (typeof bodyItem == "string") {
                        $(renderTemplate(templateRubric, {rubric: bodyItem.split("\n").join("<br>")})).appendTo($ordoItem);
                    } else {
                        $.each(bodyItem, function(x, y) {bodyItem[x] = y.replace(/\*([^\*]+)\*/g, "<em>$1</em>")})
                        $(renderTemplate(templateContentColumns, {
                            sectionVernacular: bodyItem[0].split("\n").join("<br>"),
                            sectionLatin: bodyItem[1].split("\n").join("<br>")
                        })).appendTo($ordoItem);
                    }
                });
                $ordoItem.appendTo($main);
            });
            adaptSectionColumns();
            hideLoader();
        });
    }

    $(window).on("resize", function(){
        adaptSectionColumns();
    });

    $("input[type=radio][name=lang-switch]").change(function() {
        toggleLangSections(this);
    });

    $window.on("hashchange", function() {
        let itemId = document.location.hash.replace("#", "");
        $("#sidebar li.sidebar-ordo-item").removeClass("active");
        $("#sidebar-ordo-item-" + itemId).addClass("active");
        let ordoItem = $("#ordo-item-"+itemId);
        if (navbarIsCollapsed()) {
            $sidebarAndContent.removeClass("active");
        }
        // need to wait a bit until the columns are resized back after closing the sidebar
        setTimeout(function() {$(window).scrollTop(ordoItem.offset().top - 70);}, 350);
    });

    $(window).scroll(function() {
        /**
         * Highlight displayed section in the menu
         **/
        if(scrollTimer) {
            window.clearTimeout(scrollTimer);
        }

        scrollTimer = window.setTimeout(function() {
            let windowPosition = $(this).scrollTop();
            let scrolledSections = $.grep($('.ordo-item'), function (v) {
                return windowPosition >= $(v).offset().top - 150;
            });
            let displayedSection = $(scrolledSections).last();
            let displayedSectionId = displayedSection.attr('id');
            $("#sidebar li.sidebar-ordo-item").removeClass("active");
            let sidebarItem = $("#sidebar-" + displayedSectionId);
            sidebarItem.addClass("active");
            let sidebarItemPosition = sidebarItem.position().top;
            let sidebarPosition = Math.abs($sidebar.find("ul").position().top);
            if ((sidebarItemPosition > $sidebar.height() * 0.6) || sidebarItemPosition < 0) {
                $sidebar.animate({scrollTop: sidebarPosition + sidebarItemPosition - 100}, 200);
            }
        }, 100);
    });

    $("#print").on("click", function () {
        let newWindow = window.open('','', "width=650, height=750");
        let newContent = renderTemplate(templateContentPrint, {main: $main.html()});
        newWindow.document.write(newContent);
        newWindow.document.close();
        newWindow.focus();
        return true;
    });

});