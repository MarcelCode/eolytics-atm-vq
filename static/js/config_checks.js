function check_product_poygonstatistic() {
    let products = $('.form-check-input:input[name="product_list"]');
    $.each(products, function (key, value) {
        if (!$(value).attr("checked")) {
            let polygon_el =
                $('.form-check-input:input').filter(function () {
                    return (this.name === 'polygonstatistics_products' && this.value === $(value).attr("value"))
                });
            if (polygon_el.length === 1) {
                let def_el = $(polygon_el[0]);
                def_el.prop("checked", false);
                def_el.prop("disabled", true)
            }
        }
    });
};

$(function () {
    $("input").click(function () {
        let $this = $(this);
        let formula_id = $this.attr("id").replace("calibrate", "formula");
        if (($this.attr("name").startsWith("calibrate")) && ($this.prop("checked"))) {
            $("#" + formula_id).attr("required", true);
            $("#" + formula_id).attr("disabled", false);
        } else if (($this.attr("name").startsWith("calibrate")) && !($this.prop("checked"))) {
            $("#" + formula_id).removeAttr("required");
            $("#" + formula_id).attr("disabled", true);
            $("#" + formula_id).val("");
        }
    });

    $( "input[id*='id_calibrate_']" ).each(function () {
        let $this = $(this);
        if (!$this.prop("checked")){
            let formula_id = $this.attr("id").replace("calibrate", "formula");
            $("#" + formula_id).attr("disabled", true);
        }
    });

    $("#id_scaled_workflow").click(function () {
        if ($(this).prop("checked")) {
            $("#id_pan_sharpening").attr("disabled", true)
        } else {
            $("#id_pan_sharpening").attr("disabled", false)
        }
    });

    $("#id_pan_sharpening").click(function () {
        if ($(this).prop("checked")) {
            $("#id_scaled_workflow").attr("disabled", true)
        } else {
            $("#id_scaled_workflow").attr("disabled", false)
        }
    });

    check_product_poygonstatistic();

    $('.form-check-input:input[name="product_list"]').change(function () {
        let clicked_el = $(this);
        let value = $(this).attr("value");
        let polygon_el = $('.form-check-input:input').filter(function () {
            return (this.name === 'polygonstatistics_products' && this.value === value)
        });
        if (polygon_el.length === 1) {
            let def_el = $(polygon_el[0]);
            if (clicked_el.prop("checked")) {
                def_el.prop("disabled", false);
            } else {
                def_el.prop("checked", false);
                def_el.prop("disabled", true)
            }
        }
    })
});