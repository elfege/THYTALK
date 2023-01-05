

$("#searchNews").on('keypress', function (e) {
    if (e.which == 13) {
        newsSearchHandler(e)
    }
})

// $("#searchNews").submit(newsSearchHandler)
$("#searchNewsButton").click(newsSearchHandler)

let keyword = ""
let lastIndex = 0
let articles_search; 

async function newsSearchHandler(e) {
    e.preventDefault()

    keyword = $(searchNews).val()
    console.log("NEWS SEARCHS val => ", keyword)


    const resp = await axios.get(`/talk/api/search_news/${keyword}`)
    console.log("resp news search:")
    console.log(resp)


    if (resp.data.state == "noresults") {
        overlayOn("No results were found for " + keyword)     // overlay message
        setTimeout(overlayOff, 800)
    }
    if (resp.data.state == "loginrequired") {
        overlayOn("You must login first")     // overlay message
        setTimeout(overlayOff, 800)
    }
    else if (resp.data.state == "alreadyliked") {
        overlayOn("You already liked this post")     // overlay message
        setTimeout(overlayOff, 800)
    }
    else {
        const imageDiv = $(".imgArticle")
        imageDiv.empty()
        const articlePubDate = $(".articlePubDate")
        articlePubDate.empty()
        const articleDescription = $(".articleDescription")
        articleDescription.empty()
        const articleSave = $(".articleSave")
        articleSave.empty()

        articles_search = resp.data.articles

        for (let i = 0; i < articles_search.length && i < imageDiv.length; i++) {

            const article = articles_search[i]
            console.log("this article: ", article)

            let urlToImage = article.urlToImage
            console.log("urlToImage type of ?", typeof urlToImage)

            console.log("urlToImage = ", urlToImage)
            console.log("imageDiv[" + i + "] => ", $(imageDiv[i]))

            // imageDiv[i].prepend($('<img>').addClass('img-fluid float-left imgArticle').attr("src", "https://a.fsdn.com/sd/topics/bitcoin_64.png"))

            $(imageDiv[i]).append(`<img src='${article.urlToImage}' class='img-fluid float-left imgArticle' alt=''/>`)
            $(articleDescription[i]).append(`<a class="links" href="${article.url}"><strong>${article.description}</a></strong>`)
            $(articlePubDate[i]).append(`<u>${article.publishedAt.trim("Z").replace("T", "")}</u>`)
            
            lastIndex = i
        }
        setScrollHandler()
    }
    
}


// const newsDiv = $("#mainNewsDiv")
const newsDiv = $("#mainNewsDiv")
newsDiv.off() // always off when page is reloaded
let handlerHasRun = false
function setScrollHandler() {

    newsDiv.on("scroll", () => {

        if(lastIndex < articles_search.length){
        setTimeout(resetHandlerBool, 500)
        }
        newsDiv.off() // prevent handler from running axios request for every bit scrolled; run once

        scrollFunction()

    })
}


function resetHandlerBool() {
    handlerHasRun = false
    setScrollHandler()
}

let lastKnownScrollPosition = 0;
const scrollMaxY = $("body").height();
async function scrollFunction(event) {

    /******************DELETE************************ */
    // keyword = "bitcoin" // TEST DELETE ONCE DONE
    /* ****************************************** */

    const coord = newsDiv.scrollTop()

    // console.log("coord =", coord)
    // console.log("limit =", scrollMaxY)
    // console.log("lastKnownScrollPosition = ", lastKnownScrollPosition)

    if (!handlerHasRun && lastKnownScrollPosition < coord && coord >= scrollMaxY) {
        console.log("down...")
        handlerHasRun = true

        // const controller = new AbortController()
        // const resp = await axios.get(`/talk/api/search_news/${keyword}`, {
        //     signal: controller.signal
        // })       

        console.log("articles_search => ", articles_search)

        const newsCardSection = $("#newsCardSection")

        let i = lastIndex
        for (; i < lastIndex + 20 && i < articles_search.length; i++) {


            const article = articles_search[i]

            const urlToImage = article.urlToImage
            const url = article.url
            const description = article.description
            const publishedAt = article.publishedAt.trim("Z").replace("T", "")

            console.log(`
            -------------------------
            urlToImage = ${urlToImage}
            url = ${url}
            description = ${description}
            publishedAt = ${publishedAt}
            -------------------------
            `)



            console.log("this article => ", article)

            newsCardSection.append(`
                <div class="col-9 imgArticle">
                    <img src="${urlToImage}" class="img-fluid float-left" alt="" />
                </div>

                <div class="col-9 artticleDescription">
                    <p class="h6"><a class="links"
                        href="${url}"><strong>${description}</a></strong></p>
                    <div class="articlePubDate">
                        <u>${publishedAt}</u>
                    </div>
                </div>

                <div class="col-6">
                    <button class="btn glyphicon glyphicon-save savearticle_cls" id="savearticle${i}"
                        data-article-url="${article.url}" data-article-title="${article.title}"></button>
                </div>
            `)

            
                $(`#savearticle${i}`).click(handleSaveButton)


        }

        lastIndex = i

        console.log("lastIndex => ", lastIndex)

        if(lastIndex >= articles_search.length){
            newsDiv.off() // done!
        }




        // putArticlesOnPage();


    }
    else {
        console.log("up")
    }

    lastKnownScrollPosition = newsDiv.scrollTop()


}

