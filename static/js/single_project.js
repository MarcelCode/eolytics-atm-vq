$(function () {
    function createMenu(items, ews_mission_pk) {
        return {
            callback: function (key, options) {
                axios.post('/mission/action/', {
                    ews_mission_pk: ews_mission_pk,
                    action: key
                }).then(function (response) {
                        if (response.data.status === false) {
                            Swal.fire({
                                type: 'error',
                                title: 'Maximum Core usage reached!',
                                text: response.data.message
                            })
                        } else {
                            setTimeout(function () {
                                location.reload();
                            }, 1000);
                        }
                    }
                )
            },
            items: items
        };
    }

    // some asynchronous click handler
    $( document ).on("click", '.menu-mission', function (e) {
        e.preventDefault();
        let $this = $(this);
        let ews_mission_pk = $this.data("ews-id");
        let ews_mode = $("#ews-mode").prop("checked");
        axios.post('/mission/check/', {
            ews_mode: ews_mode,
            ews_mission_pk: ews_mission_pk,
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
