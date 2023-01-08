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


$(".likepost").click(handleButton)
$(".dislikepost").click(handleButton)
$(".deletepost").click(handleButton)
$(".flagpost").click(handleButton)
$(".likereply").click(handleButton)
$(".dislikereply").click(handleButton)
$(".deletereply").click(handleButton)
$(".flagreply").click(handleButton)
$(".replypost").click(handleButton)
$(".commentArticle").click(handleButton)
$("#newPost").click(handleButton)
$(".likearticle").click(handleButton)


async function handleButton(e) {
    e.preventDefault();


    const btn = this.id
    const postId = $(`#${btn}`).attr("data-post-id") // sql id
    //distinction sql/html id is needed to dynamically add replies' divs/forms before submit
    const sql_post_container_Id = `post_container${postId}` // sql based dom id of the post container
    console.log("sql_post_container_Id ----->", sql_post_container_Id)
    const html_post_container_Id = $(`#${sql_post_container_Id}`).attr("data-html-id") // data attr based html id
    const html_postId = `post${postId}` // (both html and sql id of the post)    
    const responseId = $(`#${btn}`).attr("data-response-id")
    const html_responseId = `response${responseId}`
    const user_id = $(`#${btn}`).attr("data-user-id")
    const article_title = $(`#${btn}`).attr("data-article-title")


    console.log("********************************************")
    console.log()
    console.log("this.name ---------------------->", this.name)
    console.log("btn ---------------------------->", btn)
    console.log("html_postId -------------------->", html_postId)
    console.log("responseID --------------------->", responseId)
    console.log("sql_post_container_Id ---------->", sql_post_container_Id)
    console.log("html_post_container_Id --------->", sql_post_container_Id)
    console.log("html_responseId ---------------->", html_responseId)
    console.log("user_id ------------------------>", user_id)
    console.log("article_title ------------------>", article_title)
    console.log()
    console.log("********************************************")

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
            $(`#${sql_post_container_Id}`).remove()
            overlayOn("Post deleted!")
        }
        else {
            console.log("action canceled")
        }


    }

    if (this.name === "replypost") {

        $(`#replyDiv${postId}`).removeAttr("hidden")

        $(`#replySubmitBtn${postId}`).click(() => {
            $(`#replyDiv${postId}`).attr("hidden", "true")
        })


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

    if (this.name === "commentArticle") {

        const button = $(`#${btn}`)

        const title = button.attr("data-article-title")
        const url = button.attr("data-article-url")
        const imgurl = button.attr("data-article-imgurl")
        const description = button.attr("data-article-description")

        console.log("title:", title)
        console.log("url:", url)
        console.log("img:", imgurl)
        console.log("img:", description)

        $("#commentNewsTitle").text(title)
        $("#commentNewsImage").attr("src", imgurl)
        $("#commentNewsDescription").text(description)

        $("#commentNewsTitleValue").val(title)
        $("#commentNewsURL_Value").val(url)
        $("#commentNewsImageValue").val(imgurl)
        $("#commentNewsDescriptionValue").val(description)

        $(`#news_post`).removeAttr("hidden")

        if (smartDevice) {
            window.location.href = '#news_post'
        }


    }

    if (this.name == "newPost") {
        const button = $(`#${btn}`)

        $(`#newPostDiv`).removeAttr("hidden")
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


$("#goto_saved_art_nav").click(() => {
    openNav();

    setTimeout(scrollToArticleBtn, 500)
});

function scrollToArticleBtn() {
    const container = $("#leftSidebar")
    const scrollTo = $("#savedArticlesSubmenu_mobile_btn");

    // Calculating new position 
    // of scrollbar
    const position = scrollTo.offset().top
        - container.offset().top
        + container.scrollTop();

    // Animating scrolling effect
    container.animate({
        scrollTop: position
    });

    scrollTo.click()

    // window.location.href='#leftSidebar'
    // window.location.href='#savedArticlesSubmenu_mobile_btn'
    // $("#savedArticlesSubmenu_mobile_btn").scroll()
}


$(document).ready(() => $("#subusermenu").click()) 