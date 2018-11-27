

$(document).ready(function()    {

    const templateSectionTitle = $("#template-section-title").text();
    const templateSectionSubTitle = $("#template-section-subtitle").text();
    const templateRubric = $("#template-rubric").text();
    const templateContentColumns = $("#template-content-columns").text();

    loadOrdo();

    /**
     * Render template, substitute placeholders with elements from `data` object.
     * Example:
     * ```render('<a href="${url}">x</a>', {"url": "http://foo.com"}) -> <a href="http://foo.com">x</a>
     * Idea from https://stackoverflow.com/a/39065147
     **/
    function renderTemplate(template, data) {
        function _render(props) {
            return function (tok, i) {
                return (i % 2) ? props[tok] : tok;
            };
        }
        let parsedTpl = template.split(/\$\{(.+?)\}/g);
        return parsedTpl.map(_render(data)).join('');
    }

    function loadOrdo() {
        $.getJSON( "data/ordo.json", function( data ) {
            let $main = $("main");
            $main.empty();
            window.scrollTo(0, 0);
            $(renderTemplate(templateSectionTitle, {})).appendTo($main);
            $.each(data, function(ii, item) {
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
        });
    }
});
