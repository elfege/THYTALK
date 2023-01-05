const smartDevice = /android|webos|iphone|ipad|ipod|blackberry|iemobile|opera mini/i.test(navigator.userAgent.toLowerCase());

$(document).ready(function () {
    var open = $('.open-nav'),
        close = $('.close'),
        overlay = $('.overlay');

    open.click(function () {
        overlay.show();
        $('#wrapper').addClass('toggled');
    });

    close.click(function () {
        overlay.hide();
        $('#wrapper').removeClass('toggled');
    });
});


$(".likepost").click(handlePostButton)
$(".dislikepost").click(handlePostButton)
$(".deletepost").click(handlePostButton)
$(".flagpost").click(handlePostButton)
$(".likereply").click(handlePostButton)
$(".dislikereply").click(handlePostButton)
$(".deletereply").click(handlePostButton)
$(".flagreply").click(handlePostButton)
$(".replypost").click(handlePostButton)

async function handlePostButton(e) {
    e.preventDefault();

    console.log("this.name = ", this.name)

    const btn = this.id
    console.log("btn -----------> ", btn)

    let postId = $(`#${btn}`).attr("data-post-id") // sql id
    let html_post_container_Id = `post_container${postId}` // html doc id of the post's container
    let html_postId = `post${postId}` //html doc id of the post itself
    console.log("html_postId => ", html_postId)

    let responseId = $(`#${btn}`).attr("data-response-id")
    let html_responseId = `response${responseId}`

    console.log("responseID = ", responseId)
    console.log("html_responseId = ", html_responseId)

    /* POST LIKES DISLIKES AND DELETE */
    if (this.name === "likepost") {

        const resp = await axios.post(`/api/posts/like/${postId}`)
        console.log("response: ", resp.data)
        $(`#${btn}`).text(" " + resp.data.likes + " ")


        if (resp.data.state == "loginrequired") {
            overlayOn("You must login first")     // overlay message
            $(`#${btn}`).prop("title", "Log in first") // infobulle/tooltip 
        }
        if (resp.data.state == "alreadyliked") {
            // overlayOn("You already liked this post")     // overlay message
            // $(`#${btn}`).prop("title", "You already liked this post")
            $(`#${btn}`).text(" " + resp.data.likes + " ")
        }


    }
    if (this.name === "dislikepost") {
        const resp = await axios.post(`/api/posts/dislike/${postId}`)
        console.log("response: ", resp.data)
        $(`#${btn}`).text(" " + resp.data.dislikes + " ")
        if (resp.data.state == "loginrequired") {
            overlayOn("You must login first")     // overlay message
            $(`#${btn}`).prop("title", "Log in first") // infobulle/tooltip 
            setTimeout(overlayOff, 800)

        }
        if (resp.data.state == "alreadydisliked") {
            overlayOn("You already downvoted this post")     // overlay message
            $(`#${btn}`).prop("title", "You already liked this post")
            setTimeout(overlayOff, 800)
        }

    }
    if (this.name === "flagpost" || this.name === "deletepost") {


        text = "Are you sure you want to delete this post? This is irreversible!"
        if (confirm(text) == true) {
            await axios.delete(`/api/posts/${postId}`)
            $(`#${html_post_container_Id}`).remove()
            overlayOn("Post deleted!")
        }
        else {
            console.log("action canceled")
        }


    }

    if (this.name === "replypost") {
        // const resp = await axios.post(``)

        const action = 'post.id'
        const formLabel = 'form.hidden_tag()'


        const form = `
            <div class="container mb-5">
                <div class="row">
                <form action="/api/reply/${postId}" method="POST">
                    <div class="col-xs-8">
                        

                            <textarea rows="4" cols="50" name="response"></textarea>
                            
                    </div>
                    <div class="col-xs-2">      
                            <button type="submit" onclick="submit()" class="btn btn-default" type="button">
                                <span class="glyphicon glyphicon-send"></span> Submit </button>
                            </button>
                    </div>
                    
                    </form>
                </div>
                <div class="row">
                    
                    <div class="col-xs-6">
                            <button class="btn btn-default" onclick="location.reload()">
                                <span class="glyphicon glyphicon-remove-sign"></span> Cancel </button>
                            </button>
                            
                    </div>
                </div>
            </div>

        `

        $(`#${html_postId}`).parent().parent().parent().append(`<div class="row ml-5" id="ReplyDiv">`)
        $("#ReplyDiv").append(form)

    }


    /* REPLIES LIKES / DISLIKES / TRASH / FLAG */
    if (this.name == "likereply") {
        const resp = await axios.post(`/api/replies/like/${responseId}`)
        console.log("response: ", resp.data)
        console.log("resp.data.likes => ", resp.data.likes)
        console.log("resp.data.state => ", resp.data.state)
        $(`#${btn}`).text(" " + resp.data.likes + " ")
        if (resp.data.state == "loginrequired") {
            overlayOn("You must login first")     // overlay message
            $(`#${btn}`).prop("title", "Log in first") // infobulle/tooltip 
            setTimeout(overlayOff, 800)
        }
        if (resp.data.state == "alreadyliked") {
            console.log("deleting like to this reply")
            // overlayOn("You already liked this post")     // overlay message
            // $(`#${btn}`).prop("title", "You already liked this post")
            // setTimeout(overlayOff, 800)
            $(`#${btn}`).text(" " + resp.data.likes + " ")
        }
    }
    if (this.name === "dislikereply") {
        const resp = await axios.post(`/api/replies/dislike/${responseId}`)
        console.log("response: ", resp.data)
        $(`#${btn}`).text(" " + resp.data.dislikes + " ")
        if (resp.data.state == "loginrequired") {
            overlayOn("You must login first")     // overlay message
            $(`#${btn}`).prop("title", "Log in first") // infobulle/tooltip 
            setTimeout(overlayOff, 800)
        }
        if (resp.data.state == "alreadydisliked") {
            overlayOn("You already downvoted this post")     // overlay message
            $(`#${btn}`).prop("title", "You already liked this post")
            setTimeout(overlayOff, 800)
        }
    }
    if (this.name === "flagreply" || this.name === "deletereply") {
        await axios.delete(`/api/replies/${responseId}`)
        $(`#${html_responseId}`).remove()
    }
}



const all_butns = $(".savearticle_cls")
const allSaveButtons = [...all_butns]
console.log("list: ", allSaveButtons)

for (let i = 0; i < all_butns.length; i++) {
    const b = all_butns[i].id
    console.log("event listener created for btn id '", b, "'")
    $(`#${b}`).click(handleSaveButton)
}

async function handleSaveButton(e) {
    e.preventDefault()

    const btn = this.id
    console.log("btn = ", btn)

    const art_url = $(`#${btn}`).attr("data-article-url")
    const title = $(`#${btn}`).attr("data-article-title")

    const url = "/api/article/save" //${title}/${art_url}`

    console.log("url => ", art_url)
    console.log("title => ", title)

    const resp = await axios.post(url, {
        title: title,
        url: art_url
    })

    console.log("response: ", resp.data.message)

    if (resp.data.message === "loginrequired") {
        console.log("message loginrequired")
        overlayOn("You must login first")
        setTimeout(overlayOff, 1800)
    }
    else if (resp.data.message === "alreadysaved") {
        console.log("message alreadysaved")
        overlayOn("Article already saved")
        setTimeout(overlayOff, 1800)
    }
    else if (resp.data.message === "saved") {
        overlayOn("Saved!")
        const savedArticlesDiv = smartDevice ? $("#savedArticlesSubmenu_mobile") : $("#savedArticlesSubmenu")
        const l = $(".savedArticles").length
        if (smartDevice) {
            savedArticlesDiv.append(`
            <li>
            <a class="savedArticles" style="font-size:smaller;color:black;" href="${art_url}" id="saved_article${l + 1}">${title}</a>
            </li>
            `)
        } else {
            savedArticlesDiv.append(`
            <li>
                <a class="savedArticles" href="${art_url}" id="saved_article${l + 1}">${title}</a>
            </li>
            `)
        }
        setTimeout(overlayOff, 800)
    }



}

function overlayOn(text) {
    const o = $("#overlay")
    o.css("display", "block");
    $("#OverlayText").html(text)

}

function overlayOff() {
    document.getElementById("overlay").style.display = "none";
}


$(document).ready(() => $("#subusermenu").click()) 