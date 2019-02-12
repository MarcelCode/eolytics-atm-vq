$(function () {
    $("input").click(function () {
        let $this = $(this);
        let formula_id = $this.attr("id").replace("calibrate", "formula");
        if (($this.attr("name").startsWith("calibrate")) && ($this.prop("checked"))){
            $("#"+formula_id).attr("required", "true");
        }
        else if (($this.attr("name").startsWith("calibrate")) && !($this.prop("checked"))) {
            $("#"+formula_id).removeAttr("required");
        }
    });

    $("#id_scaled_workflow").click(function () {
        if ($(this).prop( "checked" )){
            $("#id_pan_sharpening").attr("disabled", true)
        }
        else{
            $("#id_pan_sharpening").attr("disabled", false)
        }
    });

    $("#id_pan_sharpening").click(function () {
        if ($(this).prop( "checked" )){
            $("#id_scaled_workflow").attr("disabled", true)
        }
        else{
            $("#id_scaled_workflow").attr("disabled", false)
        }
    })
});