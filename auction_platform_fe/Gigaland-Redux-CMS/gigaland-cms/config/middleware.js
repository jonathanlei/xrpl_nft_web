module.exports = {
    load: {
        before: ['responseTime', 'cors', 'responses'],
        order: ['responseTime', 'cors', 'responses'],
        after: ['parser', 'router'],
    },
    settings: {
        cors: {
            enabled: true,
            origin: ['*'],
            // headers: ['*']
        },
    },
};