$(function () {
    function createMenu(items, ews_mission_pk) {
        return {
            callback: function (key, options) {
                axios.post('/mission/action/', {
                    ews_mission_pk: ews_mission_pk,
                    action: key
                })
            },
            items: items
        };
    }

    // some asynchronous click handler
    $('.menu-mission').click(function (e) {
        e.preventDefault();
        let $this = $(this);
        let ews_mission_pk = $this.data("ews-id");
        let ews_state = $this.data("ews-state");
        axios.post('/mission/check/', {
            ews_mission_pk: ews_mission_pk,
            ews_state: ews_state,
            project_pk: project_pk
        }).then(function (response) {
            $this.data('runCallback', createMenu(response.data, ews_mission_pk));
            var _offset = $this.offset(),
                position = {x: _offset.left + 10, y: _offset.top + 10};
            $this.contextMenu(position);
        });
    });

    $.contextMenu({
        selector: '.menu-mission',
        trigger: 'none',
        build: function ($trigger, e) {
            e.preventDefault();

            // pull a callback from the trigger
            return $trigger.data('runCallback');
        }
    });
});
