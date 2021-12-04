'use strict';
const { sanitizeEntity } = require('strapi-utils');

/**
 * Read the documentation (https://strapi.io/documentation/developer-docs/latest/development/backend-customization.html#core-controllers)
 * to customize this controller
 */

module.exports = {

    async find(ctx) {
        const entity = await strapi.services['blog-post'].find(ctx.query, [
            'author', 'author.avatar', 'cover'
        ]);

        const sanitized = sanitizeEntity(entity, { model: strapi.models['blog-post'] });

        return sanitized;
    },
    
    async findOne(ctx) {
        const { id } = ctx.params;

        const entity = await strapi.services['blog-post'].findOne({ id }, [
            'author', 'author.avatar', 'cover'
        ]);

        const sanitized = sanitizeEntity(entity, { model: strapi.models['blog-post'] });

        return sanitized;
    },

    async comments(ctx) {
        const { id } = ctx.params;

        const entity = await strapi.services['blog-post'].findOne({ id }, [
            'post_comment', 
            'post_comment.comments', 
            'post_comment.comments.author', 
            'post_comment.comments.author.avatar', 
            'post_comment.comments.replies', 
            'post_comment.comments.replies.author',
            'post_comment.comments.replies.author.avatar'
        ]);

        const sanitized = sanitizeEntity(entity, { model: strapi.models['blog-post'] });

        const result = sanitized.post_comment.comments.filter(comment => comment.is_reply === false);
        const sorted = result.sort((a, b) => (a.updated_at > b.updated_at) ? 1 : -1);
        const comments = sorted.map(comment => {
            return {
                avatar: comment.author.avatar.url,
                username: comment.author.username,
                comment: comment.text,
                timestamp: comment.updated_at,
                replies: comment.replies.map(reply => {
                    return {
                        avatar: reply.author.avatar.url,
                        username: reply.author.username,
                        comment: reply.text,
                        timestamp: reply.updated_at
                    }
                })
            }
        });

        const response = {
            counts: sanitized.post_comment.comments.length,
            comments : comments
        };

        return response;
    },
    
    async tags(ctx) {
        const { id } = ctx.params;

        const entity = await strapi.services['blog-post'].findOne({ id }, [
            'post_tag',
            'post_tag.tags'
        ]);

        
        const sanitized = sanitizeEntity(entity, { model: strapi.models['blog-post'] });
        const tags = sanitized.post_tag.tags.map(tag => {
            return {name: tag.name}
        });

        return tags;
    },

    async recent(ctx) {
        const entity = await strapi.services['blog-post'].find(ctx.query, []);

        const sanitized = sanitizeEntity(entity, { model: strapi.models['blog-post'] });
        const recents = sanitized.slice(0,4).map(post => {
            return { title: post.title, timestamp: post.updated_at }
        });

        return recents;
    }

};
