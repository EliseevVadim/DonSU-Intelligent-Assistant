import { notify } from "@kyvg/vue3-notification";

function show(type, title, text) {
    notify({
        title: title,
        text: text,
        type: type,
        duration: 5000
    })
}

export default {
    success: (title, text, options) => show("success", title, text, options),
    warn: (title, text, options) => show("warn", title, text, options),
    error: (title, text, options) => show("error", title, text, options),
    info: (title, text, options) => show("info", title, text, options),
};