// Libraries
import React, { useState } from 'react';

// Components
import CommentForm from './CommentForm';
import EditMemeForm from './EditMemeForm';

const Card = (props) => {

    // States to show/hide the Comments section and 
    // update meme form
    const [showComments, setShowCommments] = useState(false);
    const [showEditMeme, setShowEditMeme] = useState(false);

    return (
        <div className="card" key={props.id}>
            <img src={props.url} className="mx-auto" alt="" />
            <p className="mt-5 font-semibold text-blue-500 text-md">{props.name}</p>
            <p className="w-full mt-2 text-sm">{props.caption}</p>

            <div className="mt-5 md:flex">
            <button className="card-button" 
                onClick={e => {
                    const like = {"meme_id": props.id}
                    props.postLike(like, props.likes).then(() => {
                    });
                }}
            >
                {props.likes} Likes
            </button>
            <button className="ml-2 card-button"
                onClick={e=> {
                    setShowEditMeme(false);
                    setShowCommments(!showComments);
                }}
            >
                {props.comments.length} Comments
            </button>
            <button className="ml-2 card-button"
                onClick={e=> {
                    setShowCommments(false);
                    setShowEditMeme(!showEditMeme);
                }}
            >
                Edit Meme
            </button>


            </div>
            {showComments ? (
            <div>
            {props.comments.length === 0 ? (<p></p>) : (
                <div className="mt-2 overflow-y-auto text-sm max-h-32">
                { props.comments.map(comment => (
                    <div key={comment.id}> 
                    <p className="mt-2 font-semibold">{comment.name}</p>
                    <p>{comment.content}</p>
                    </div>
                ))
                }            
                </div>    
                
            )}

            <CommentForm
                postComment={props.postComment}
                id={props.id}
            />
            </div>
            ) : (
                <div></div>
            )}
            
            {showEditMeme ? (
                <EditMemeForm
                id={props.id}
                name={props.name}
                caption={props.caption}
                url={props.url}
                updateMeme={props.updateMeme}
                />
            ) : (
                <div></div>
            )
            }
            
        </div>
    )
}

export default Card;
