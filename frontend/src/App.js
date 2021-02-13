import React from 'react';
import Basic from './Form'
import Card from './Card'
import API from './ApiServices';

function App() {
  
  const [postMemes, postComment, postLike, updateMeme, loading, memes] = API();

  return (
    <div>
      <header className="header">
        <h1 className="font-semibold">XMEME</h1>
      </header>

    <div className="md:flex">
      <Basic
        postMemes={postMemes}
      />
      <div className="p-5 md:overflow-y-auto md:h-screen md:p-20 md:w-2/4">
      { loading === "false" ? (<p>Error! couldnt retrieve memes.</p>) : 

      (
        memes.length === 0 ? (
          <div className="card">
            <img className="mx-auto" src="https://i.kym-cdn.com/photos/images/newsfeed/001/668/803/f75.jpg" alt="sad meme"></img>
          </div>
          ) :
          ( memes.map(item => (
            <Card
            key= {item.id}
            postLike={postLike}
            postComment={postComment}
            updateMeme={updateMeme}
            id={item.id}
            name={item.name}
            url={item.url}
            caption={item.caption}
            likes={item.likes}
            comments={item.comments}
            />
        )))
      )}
      </div>
    </div>

    </div>
  );
}

export default App;