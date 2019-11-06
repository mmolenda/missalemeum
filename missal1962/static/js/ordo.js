$(window).on("load", function () {

    const templateSectionTitle = $("#template-section-title").text();
    const templateSectionSubTitle = $("#template-section-subtitle").text();
    const templateRubric = $("#template-rubric").text();
    const templateContentColumns = $("#template-content-columns").text();
    const templateSidebarItem = $("#template-sidebar-ordo-item").text();
    const templateContentPrint = $("#template-content-print").text();

    loadOrdo();

    function loadOrdo() {
        showLoader();
        $.getJSON( "data/ordo.json", function( data ) {
            let $main = $("main");
            $main.empty();
            let sidebarUl = $("nav#sidebar>ul");
            sidebarUl.empty();
            window.scrollTo(0, 0);
            $(renderTemplate(templateSectionTitle, {})).appendTo($main);
            $.each(data, function(ii, item) {
                $(renderTemplate(templateSidebarItem, {id: ii, title: item.title})).appendTo(sidebarUl);
                $(renderTemplate(templateSectionSubTitle, {id: ii, title: item.title})).appendTo($main);
                $.each(item.body, function(jj, bodyItem) {
                    if (typeof bodyItem == "string") {
                        $(renderTemplate(templateRubric, {rubric: bodyItem.split("\n").join("<br>")})).appendTo($main);
                    } else {
                        $.each(bodyItem, function(x, y) {bodyItem[x] = y.replace(/\*([^\*]+)\*/g, "<em>$1</em>")})
                        $(renderTemplate(templateContentColumns, {
                            sectionVernacular: bodyItem[0].split("\n").join("<br>"),
                            sectionLatin: bodyItem[1].split("\n").join("<br>")
                        })).appendTo($main);
                    }
                });
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

    $("#print").on("click", function () {
        let newWindow = window.open('','', "width=650, height=750");
        let newContent = renderTemplate(templateContentPrint, {main: $main.html()});
        newWindow.document.write(newContent);
        newWindow.document.close();
        newWindow.focus();
        return true;
    });

});