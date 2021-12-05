'use strict';
const { sanitizeEntity } = require('strapi-utils');

/**
 * Read the documentation (https://strapi.io/documentation/developer-docs/latest/development/backend-customization.html#core-controllers)
 * to customize this controller
 */

module.exports = {
    async find(ctx) {
        const entity = await strapi.services['author-sales'].find(ctx.query, [
            'author', 'author.id'
        ]);

        const sanitized = sanitizeEntity(entity, { model: strapi.models['author-sales'] });

        return sanitized;
    }
};
