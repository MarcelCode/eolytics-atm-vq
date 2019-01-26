$(function(){
    $.contextMenu({
        selector: '.menu-mission-start',
        trigger: 'left',
        callback: function(key, options) {
            let mission_pk = $(options.$trigger).data("id");
        },
        items: {
            "start": {name: "Start"},
            "stop_block": {
                name: "Stop after Block",
                items:{
                    "stop_block1": {name: "Block 1"},
                    "stop_block2": {name: "Block 2"},
                    "stop_block3": {name: "Block 3"},
                    "stop_block4": {name: "Block 4"}
                }
            },
            "reset_block": {name: "Reset Block"},
            "config": {name: "Mission Config"}
        }
    });

    $.contextMenu({
        selector: '.menu-mission-stopped',
        trigger: 'left',
        callback: function(key, options) {
            let mission_pk = $(options.$trigger).data("id");
        },
        items: {
            "continue": {name: "Continue"},
            "restart": {name: "Restart"},
            "stop_block": {
                name: "Stop after Block",
                items:{
                    "stop_block1": {name: "Block 1"},
                    "stop_block2": {name: "Block 2"},
                    "stop_block3": {name: "Block 3"},
                    "stop_block4": {name: "Block 4"}
                }
            },
            "reset_block": {name: "Reset Block"},
            "config": {name: "Mission Config"}
        }
    });

    $.contextMenu({
        selector: '.menu-mission-finished',
        trigger: 'left',
        callback: function(key, options) {
            let mission_pk = $(options.$trigger).data("id");
        },
        items: {
            "restart": {name: "Restart"},
            "stop_block": {
                name: "Stop after Block",
                items:{
                    "stop_block1": {name: "Block 1"},
                    "stop_block2": {name: "Block 2"},
                    "stop_block3": {name: "Block 3"},
                    "stop_block4": {name: "Block 4"}
                }
            },
            "reset_block": {name: "Reset Block"},
            "config": {name: "Mission Config"}
        }
    });
});