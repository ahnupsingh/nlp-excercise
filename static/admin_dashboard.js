document.addEventListener('DOMContentLoaded', function() {
    const selector = document.getElementById('city-selector');
    selector.addEventListener('change', function() {
        const cityId = this.value;
        if (!cityId) return;
        api(cityId);
    });
});

const api = (cityId, params='', generate='') => {
    fetch(`/api/posts_by_city/${cityId}?topic=${params}&generate=${generate}`)
    .then(response => response.json())
    .then(data => {
        const container1 = document.getElementById('posts-container');
        const container2 = document.getElementById('hot-topics-container');
        const hotTopicsBlock = document.getElementById('hot-topics-block');
        hotTopicsBlock.style.display = 'block';
        container1.innerHTML = '';
        container2.innerHTML = '';
        data.posts.forEach(post => {
            const postContainer = document.createElement('div');
            postContainer.className = "border flex flex-col flex-grow p-6 rounded-md shadow-sm dark:border-gray-800";

            postContainer.onclick = function() {
                window.location.href = `/api/post_summary/${post.id}`;
            };

            const contentDiv = document.createElement('div');
            contentDiv.className = "flex-grow relative";
            contentDiv.textContent = post.topic;

            postContainer.appendChild(contentDiv);
            container1.appendChild(postContainer);
        });

        if (data.hot_topics.length == 0){
            const div = document.createElement('div');
            div.textContent = "Not hot topics found for this city";
            container2.appendChild(div);
            const buttondiv = document.getElementById('generate-hot-topics');
            buttondiv.style.display = 'block';

            const button = document.getElementsByClassName('generate-button');
            buttondiv.onclick = function() {
                api(cityId, '', generate='hot-topics')
            };
        }

        if (data.posts.length == 0){
            const div = document.createElement('div');
            div.textContent = "No any posts in this city";
            container1.appendChild(div);
            const buttondiv = document.getElementById('generate-posts');
            buttondiv.style.display = 'block';
            buttondiv.onclick = function() {
                api(cityId, '', generate='posts')
            };
            hotTopicsBlock.style.display = 'none';
        }

        data.hot_topics.forEach(topic => {
            const topicContainer = document.createElement('div');
            topicContainer.className = "border flex flex-col flex-grow p-6 rounded-md shadow-sm dark:border-gray-800 lg:w-1/3";

            topicContainer.onclick = function() {
                api(cityId, topic.topic)
            };

            const contentDiv = document.createElement('div');
            contentDiv.className = "flex-grow relative";
            contentDiv.textContent = topic.topic;

            topicContainer.appendChild(contentDiv);
            container2.appendChild(topicContainer);
        })
    })
    .catch(error => console.error('Error loading posts:', error));
}