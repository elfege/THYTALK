

$("#searchNews").on('keypress', function (e) {
    if (e.which == 13) {
        newsSearchHandler()
    }
})

// $("#searchNews").submit(newsSearchHandler)
$("#searchNewsButton").click(newsSearchHandler)

async function newsSearchHandler(e) {
    // e.preventDefault()

    const keyword = $(searchNews).val()
    console.log("NEWS SEARCHS val => ", keyword)


    const resp = await axios.get(`/talk/api/search_news/${keyword}`)
    console.log("response news search:")
    console.log(resp)



    if (resp.data.state == "loginrequired") {
        overlayOn("You must login first")     // overlay message
        $(`#${btn}`).prop("title", "Log in first") // infobulle/tooltip 
        setTimeout(overlayOff, 800)
    }
    else if (resp.data.state == "alreadyliked") {
        overlayOn("You already liked this post")     // overlay message
        $(`#${btn}`).prop("title", "You already liked this post")
        setTimeout(overlayOff, 800)
    }
    else {


        const imageDiv = $(".imgArticle")
        imageDiv.empty()
        const articlePubDate = $(".articlePubDate")
        articlePubDate.empty()
        const artticleDescription = $(".artticleDescription")
        artticleDescription.empty()
        const articleSave = $(".articleSave")
        articleSave.empty()

        const articles = resp.data.articles

        for (let i = 0; i < articles.length && i < imageDiv.length; i++) {

            const article = articles[i]
            console.log("this article: ", article)

            let urlToImage = article.urlToImage
            console.log("urlToImage type of ?", typeof urlToImage)

            console.log("urlToImage = ", urlToImage)
            console.log("imageDiv["+i+"] => ", $(imageDiv[i]))

            // imageDiv[i].prepend($('<img>').addClass('img-fluid float-left imgArticle').attr("src", "https://a.fsdn.com/sd/topics/bitcoin_64.png"))
            
            $(imageDiv[i]).append(`<img src='${article.urlToImage}' class='img-fluid float-left imgArticle' alt=''/>`)
            $(artticleDescription[i]).append(`<a class="links" href="${article.url}"><strong>${article.description}</a></strong>`)
            $(articlePubDate[i]).append(`<u>${article.publishedAt.trim("Z").replace("T", "")}</u>`)
            

        }

    }

}

let lastKnownScrollPosition;
async function scrollFunction(event) {
  console.log("scroll!")
  if(lastKnownScrollPosition < window.scrollY)
  {
    console.log("down...")
    // storyList = await StoryList.getStories();
    let newStories = await axios({
      url: `${BASE_URL}/stories`,
      method: "GET",
    });
    // console.log("newStories:", newStories.data.stories)

    for(let a of newStories.data.stories)
    {
      console.log("adding story:", a)
      await storyList.addStory(currentUser, { title: a.title, author: a.author+'bob', url: a.url });

    }
      

    putStoriesOnPage();
  }
  else{
    console.log("up")
  }
  lastKnownScrollPosition = window.scrollY

}