import { useState, useEffect } from 'react'

export const apiUrl = "http://localhost:8081";

function API() {

    const [memeID, setMemeID] = useState()
    const [commentID, setCommentID] = useState();
    const [likeID, setLikeID] = useState();
    const [updateMemeID, setUpdateMemeID] = useState();
    const [count, setCount] = useState(0);
    const [loading, setLoading] = useState("");    
    const [memes, setMemes] = useState([]);
    
    async function fetchMemes() {
      try {
        setLoading("true")
        const response = await fetch(`${apiUrl}/memes/`);
        const json = await response.json();
        setMemes(json.map(item => item))
      } catch (error) {
        setLoading("false");
      }
    }
  
    useEffect(() => {
      fetchMemes();
    }, [likeID, memeID, commentID, updateMemeID, count])
  
    async function postMemes(meme) {
        try {
            const response = await fetch(`${apiUrl}/memes/`, {
                method: "post",
                headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
                },
                body: JSON.stringify(meme)
            });
            const json = await response.json();
            setMemeID(json.id);
            alert("Meme posted");
        } catch (error) {
          setMemeID(`error : ${error}`);
        }
        return [memeID];
    }
  
    async function postComment(comment) {
      try {
          const response = await fetch(`${apiUrl}/comment/`, {
              method: "post",
              headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json'
              },
              body: JSON.stringify(comment)
          });
          const json = await response.json();
          setCommentID(`${json.meme_id}-${json.id}`);
      } catch (error) {
        setCommentID(`error : ${error}`);
      }
      return [commentID];
  }
  
  async function postLike(like, likeCount) {
      try {
          const response = await fetch(`${apiUrl}/like/`, {
              method: "post",
              headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json'
              },
              body: JSON.stringify(like)
          });            
          const json = await response.json();
          setLikeID(`${json.id}-${likeCount}`);
      } catch (error) {
        setLikeID(`error : ${error}`);
      }
      return [likeID];
  }
  
  async function updateMeme(meme) {
    try {
        const response = await fetch(`${apiUrl}/memes/`, {
            method: "PATCH",
            headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
            },
            body: JSON.stringify(meme)
        });
        const json = await response.json();
        setUpdateMemeID(`${json.id} - ${count}`);
        setCount(count+1);
        alert("Meme updated");
    } catch (error) {
      setUpdateMemeID(`error : ${error}`);
    }
    return [updateMemeID];
  }

  return [postMemes, postComment, postLike, updateMeme, loading, memes];

}

export default API;
