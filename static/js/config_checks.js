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
    })
});