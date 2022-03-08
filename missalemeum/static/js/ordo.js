$window.on("load", function () {

    const $templateContentPrint = $("#template-content-print").text();

    const $sidebar = $("nav#sidebar");
    let scrollTimer;

    adaptSectionColumns();
    showSection();

    $window.on("resize", function(){
        adaptSectionColumns();
    });

    $("input[type=radio][name=lang-switch]").change(function() {
        toggleLangSections(this.id);
    });

    function showSection() {
        let itemId = document.location.hash.replace("#", "");
        let activeSidebarItem = $("#sidebar-ordo-item-" + itemId);
        if (activeSidebarItem.length === 0) {
            return;
        }
        $("#sidebar li.sidebar-ordo-item").removeClass("active");
        activeSidebarItem.addClass("active");
        let ordoItem = $("#ordo-item-"+itemId);
        if (navbarIsCollapsed()) {
            $sidebarAndContent.removeClass("active");
        }
        // need to wait a bit until the columns are resized back after closing the sidebar
        setTimeout(function() {$window.scrollTop(ordoItem.offset().top - 70);}, 350);
    }

    $window.on("hashchange", function() {
        showSection();
    });

    $window.scroll(function() {
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
            window.history.replaceState({}, '', '' + sidebarItem.find('a').attr('href'));
            let sidebarItemPosition = sidebarItem.position().top;
            let sidebarPosition = Math.abs($sidebar.find("ul").position().top);
            if ((sidebarItemPosition > $sidebar.height() * 0.6) || sidebarItemPosition < 0) {
                $sidebar.animate({scrollTop: sidebarPosition + sidebarItemPosition - 100}, 200);
            }
        }, 100);
    });

    $("#print").on("click", function () {
        printContent($templateContentPrint, $loadedContent.html());
    });

});