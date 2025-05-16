document.addEventListener("DOMContentLoaded", function() {
    const containers = document.querySelectorAll("[id^='env-'][id$='-container'], [id^='media-'][id$='-container'], [id^='calc-'][id$='-container']");
    containers.forEach(container => {
        const width = container.getBoundingClientRect().width;
        const height = container.getBoundingClientRect().height;
        const containerId = container.id;

        fetch('/report-dimensions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                container_id: containerId,
                width: width,
                height: height
            })
        });
    });
});