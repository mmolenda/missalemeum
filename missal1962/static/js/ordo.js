$(window).on("load", function () {

    const templateSectionTitle = $("#template-section-title").text();
    const templateSectionSubTitle = $("#template-section-subtitle").text();
    const templateRubric = $("#template-rubric").text();
    const templateContentColumns = $("#template-content-columns").text();
    const templateSidebarItem = $("#template-sidebar-ordo-item").text();

    loadOrdo();

    function loadOrdo() {
        $.getJSON( "data/ordo.json", function( data ) {
            let $main = $("main");
            $main.empty();
            let sidebarUl = $("nav#sidebar>ul");
            sidebarUl.empty();
            window.scrollTo(0, 0);
            $(renderTemplate(templateSectionTitle, {})).appendTo($main);
            $.each(data, function(ii, item) {
                $(renderTemplate(templateSidebarItem, {title: item.title})).appendTo(sidebarUl);
                $(renderTemplate(templateSectionSubTitle, {title: item.title})).appendTo($main);
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
        });
    }

    $(window).on("resize", function(){
        adaptSectionColumns();
    });

    $("input[type=radio][name=lang-switch]").change(function() {
        toggleLangSections(this);
    });

});