<template>
    <div class="steps-main-wrapper flex flex-column">
        <Steps :model="items" :readonly="true">
            <template #item="{ item, active }">
                <div class="inline-flex align-items-center justify-content-center align-items-center border-circle border-primary border-1  h-3rem w-3rem z-1 cursor-pointer" :class = '{ "bg-primary" : item.status, "text-primary surface-overlay" : !item.status }'>
                    <i :class="[item.icon, 'text-xl']" />
                </div>
            </template>
        </Steps>
        <div class="step-titles flex justify-content-around">
            <div class = "step-title-box flex flex-column align-items-center">
                {{ this.entity }} Uploaded 
                <small>{{ items[0].small }}</small>
                <Button text raised class = "step-btn" v-if = "!items[2].status" @click = "toDetails">Preview {{ this.entity }}</Button>
            </div>

            <div class = "step-title-box flex flex-column align-items-center">
                Admin Approval
                <small :class = "{'text-yellow-600' : items[1].status == false, 'text-red-500': items[1].status == 'deny'}">{{ items[1].small }}</small>
                <Button class = "feedback-display-btn step-btn" text raised v-if = "items[1].status == 'deny'" @click = "displayFeedback">See Feedback</Button>
            </div>
            <Dialog v-model:visible="feedbackDialogVisible" modal header="Admin's feedback" :style="{ width: '25rem' }">
                <div class="flex align-items-center gap-3 mb-3">
                    {{ feedbackText }}
                </div>
            </Dialog>

            <div class = "step-title-box flex flex-column align-items-center">
                {{ this.entity }} Finalized
                <small :class = "{'text-yellow-600' : items[2].status == false}">{{ items[2].small }}</small>
                <Button class = "step-btn" text raised v-if = "items[2].status" @click = "toDetails">{{ this.entity }} Details</Button>
            </div> 
        </div>
    </div>
</template>

<script>
import Steps from 'primevue/steps'
import Button from 'primevue/button'
import Dialog from 'primevue/dialog'
import axios from 'axios'
export default {
    props: {product: Object, adminApproval: String, productId: String, entity: String },
    components: { Dialog, Steps, Button },
    data(){
        return {
            completedIcon: 'pi pi-check',
            completeTheme: 'bg-primary',
            items: [
                {icon: 'pi pi-upload', status: true, small: 'Completed'}, 
                {icon: 'pi pi-users', status: false, small: 'Pending'}, 
                {icon: 'pi pi-check-square', status: false, small: 'Pending'}
            ],
            feedbackDialogVisible: false,
            feedbackText: '',
        }
    },
    created(){
        if(this.adminApproval == "True"){
            this.items[1].status = 'true'
            this.items[2].status = 'true'
            this.items[1].small= 'Completed'
            this.items[2].small= 'Completed'
        }

        if(this.adminApproval == "Deny"){
            this.items[1].status = 'deny'
            this.items[1].small= 'Denied'
        }
    },

    methods:{
        toDetails(){
            if(this.entity == "Listing")
                this.toListingDetails()
            else
                this.toResourceDetails()
        },

        displayFeedback(){
            if(this.entity == "Listing")
                this.listingFeedback()
            else
                this.resourceFeedback()
        },

        listingFeedback(){
            axios.get(`http://localhost:8000/admin_actions/get_negative_feedback/${this.productId}`)
            .then(response => {
                this.feedbackText = response.data.feedback
            })
            .catch(error => console.log(error))
            this.feedbackDialogVisible = true
        },

        resourceFeedback(){
            //yes resource id is stored in productId
            axios.get(`http://localhost:8000/admin_actions/get_negative_feedback_resource/${this.productId}`)
            .then(response => {
                this.feedbackText = response.data.feedback
            })
            .catch(error => console.log(error))
            this.feedbackDialogVisible = true
        },

        toListingDetails(){
            //WatchMojo: Top 10 reasons why you should learn regex
            const image_url =  this.product.image_urls.replaceAll("'", "").replaceAll("[", "").replaceAll("]", "").replaceAll('"', "").split(", ")
            const selectedYear = this.product.selected_year.replaceAll("'", "").replaceAll("[", "").replaceAll("]", "").replaceAll('"', "").split(", ")
            const selectedBranch = this.product.selected_branch.replaceAll("'", "").replaceAll("[", "").replaceAll("]", "").replaceAll('"', "").split(", ")
            const selectedItemType = this.product.selected_item_type.replaceAll("'", "").replaceAll("[", "").replaceAll("]", "").replaceAll('"', "").split(", ")
            const selectedCondition = this.product.selected_condition.replaceAll("'", "").replaceAll("[", "").replaceAll("]", "").replaceAll('"', "")
            const sessionInfo = JSON.parse(sessionStorage.user)
            this.$router.push({ name: "Listing details", params: {
                product: JSON.stringify({
                    moodleID: sessionInfo.user.moodleID,
                    title: this.product.title,
                    category: this.product.category,
                    price: this.product.price,
                    productDesc: this.product.product_description,
                    selectedYear: selectedYear,
                    selectedBranch: selectedBranch,
                    selectedItemType: selectedItemType,
                    selectedCondition: selectedCondition,
                    image_urls: image_url, 
                }),
                adminStatus:this.items[1].status,
                id: this.productId,
            }})
        },

        toResourceDetails(){
            this.$router.push({ name: "Resource Details", params: {
                resourceId: this.productId,
                adminStatus: this.items[1].status
            }})
        },
    },
}
</script>

<style>
.step-title-box small{
    color: green;
    margin: 0.2rem 0rem;
    /* margin-right: 0.5rem; */
    text-align: center;
}

.step-title-button{
    margin-top: 0.5rem;
}
.p-steps-list{
    height: 10vh;
}

</style>