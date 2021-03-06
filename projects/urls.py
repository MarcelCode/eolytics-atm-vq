from django.urls import path
from projects import views

urlpatterns = [
    path("projects/<slug:status>/", views.projects, name="projects"),
    path("projects/<slug:status>/remove/<int:project_pk>/", views.delete_project, name="delete-project"),
    path("project/<int:project_pk>/", views.project, name="project"),
    path("project/<int:project_pk>/automatic-mode/", views.automatic_mode, name="automatic-mode"),
    path("project/<int:project_pk>/config/<int:config_pk>/", views.project_settings, name="config-pk"),
    path("project/<int:project_pk>/config/<int:config_pk>/<slug:action>/", views.project_settings,
         name="config-action"),
    path("project/<int:project_pk>/download/", views.download_data_for_project, name="project-download"),
    path("project/<int:project_pk>/download/upload-aoi", views.upload_aoi_download, name="upload-aoi-download"),

    path("project/<int:project_pk>/download/status", views.download_status_for_project, name="project-download-status"),
    path("project/<int:project_pk>/download/status-single", views.download_status_single,
         name="project-download-single"),
    path("project/<int:project_pk>/download/status-continuous", views.download_status_continuous,
         name="project-download-continuous"),

    path("project/<int:project_pk>/download/final", views.download_final_results, name="project-download-final"),

    path("project/<int:project_pk>/download/cancel", views.download_cancel, name="project-download-cancel"),
    path("project/<int:project_pk>/download/cancel-auto", views.download_cancel_continuous,
         name="project-download-cancel-auto"),

    path("project/<int:project_pk>/masking/<int:masking_pk>/", views.masking_settings, name="masking-pk"),
    path("project/<int:project_pk>/masking/<int:masking_pk>/<slug:action>/", views.masking_settings,
         name="masking-action"),

    path("project/create_project/", views.create_project, name="create-project"),
    path("project/memory_info/", views.get_memory_info, name="memory-info"),

    path("project/reset-missions/", views.reset_mission_by_state, name="reset-missions"),

    path("project/change_cores/", views.change_project_cores, name="change-cores"),
]
