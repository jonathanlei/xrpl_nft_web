'use strict';
const { sanitizeEntity } = require('strapi-utils');

/**
 * Read the documentation (https://strapi.io/documentation/developer-docs/latest/development/backend-customization.html#core-controllers)
 * to customize this controller
 */

module.exports = {
    async find(ctx) {
        const entity = await strapi.services.author.find(ctx.query);

        const sanitized = sanitizeEntity(entity, { model: strapi.models.author });
        const sorted = sanitized.sort((a, b) => (a.author_sale.sales < b.author_sale.sales) ? 1 : -1);

        return sorted;
    },
    
    async ranks(ctx) {
        const entity = await strapi.services.author.find(ctx.query, [
            'author_sale', 'avatar'
        ]);

        const sanitized = sanitizeEntity(entity, { model: strapi.models.author });
        const sorted = sanitized.sort((a, b) => (a.author_sale.volume < b.author_sale.volume) ? 1 : -1);

        return sorted;
    }
};
