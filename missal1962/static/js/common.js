
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

/**
 * For large screens show both language columns adjacently.
 * For small screens show columns only for the language selected
 * in `#lang-switch`
 **/
function adaptSectionColumns() {
    if ($(window).width() >= 576) {
        $("div.section-vernacular").show();
        $("div.section-latin").show();
    } else {
        let langId = $("#lang-switch>label.active>input").attr("id");
        if (langId == "lang-switch-vernacular") {
            $("div.section-vernacular").show();
            $("div.section-latin").hide();
        } else {
            $("div.section-vernacular").hide();
            $("div.section-latin").show();
        }
    }
}

/**
 * Switch between lang versions on small screens, where the switch is visible
 **/
function toggleLangSections(input) {
    if (input.id == "lang-switch-vernacular") {
        $("div.section-vernacular").show();
        $("div.section-latin").hide();
    } else {
        $("div.section-vernacular").hide();
        $("div.section-latin").show();
    }
}