<script>
import addSub from "../components/addSub.vue"
import subList from "../components/subList.vue"
export default{
    components: {addSub, subList},
    async setup(){
        const config = await fetch("http://localhost:3000/config").then(res => res.json())
        return {
            config
        }
    }   
}
</script>
<template>

        <h4>client_id: {{ config["client_id"] }}</h4>
        <h4>client_secret: {{ config["client_secret"] }}</h4>
        <h4>password: {{ config["password"] }}</h4>
        <h4>user_agent: {{ config["user_agent"] }}</h4>
        <h4>username: {{ config["username"] }}</h4>
        <div>
            <ul>
                <subList v-for="sub in config['subreddits']"
                         :name=sub />
            </ul>
            <addSub />
        </div>
</template>