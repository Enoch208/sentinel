use std::fs::File;
use std::process::{Child, Command, Stdio};
use std::sync::Mutex;

use tauri::path::BaseDirectory;
use tauri::{Manager, RunEvent};

struct Engine(Mutex<Option<Child>>);

fn spawn_engine(app: &tauri::AppHandle) -> Option<Child> {
    let exe = app
        .path()
        .resolve("engine/sentinel-serve", BaseDirectory::Resource)
        .ok()?;
    if !exe.exists() {
        return None;
    }
    let model = app.path().resolve("model", BaseDirectory::Resource).ok()?;
    let data = app.path().app_data_dir().ok()?;
    let _ = std::fs::create_dir_all(&data);

    let mut command = Command::new(exe);
    command
        .env("SENTINEL_CACHE", model)
        .env("SENTINEL_DB", data.join("sentinel.db"))
        .current_dir(&data);

    if let Ok(log) = File::create(data.join("engine.log")) {
        if let Ok(err) = log.try_clone() {
            command.stdout(Stdio::from(log)).stderr(Stdio::from(err));
        }
    }

    command.spawn().ok()
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .setup(|app| {
            let child = spawn_engine(app.handle());
            app.manage(Engine(Mutex::new(child)));
            Ok(())
        })
        .build(tauri::generate_context!())
        .expect("error while building the Sentinel app")
        .run(|app, event| {
            if let RunEvent::Exit = event {
                if let Some(engine) = app.try_state::<Engine>() {
                    if let Ok(mut guard) = engine.0.lock() {
                        if let Some(mut child) = guard.take() {
                            let _ = child.kill();
                        }
                    }
                }
            }
        });
}
