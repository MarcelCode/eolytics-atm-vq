$(function () {
    $.contextMenu({
        selector: '.context-menu-scenes',
        callback: function (key, options) {
            var m = "clicked: " + key;
            window.console && console.log(m)
        },
        items: {
            "start": {name: "Start"},
            "start_w_a": {name: "Start with action"},
            "stop": {name: "Stop"},
            "show_log": {name: "Show logfile"},
            "delete_log": {name: "Delete logfile"},
            "tools": {
                name: "Tools",
                items: {
                    "move_ignore": {name: "Move to ignore"},
                    "move_delete": {name: "Move to ignore and delete from HD"},
                    "delete": {name: "Delete from HD"},
                }
            }
        }
    });
});



