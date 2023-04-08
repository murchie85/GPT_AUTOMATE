const Comment = (props) => {
  const [showCommentBox, setShowCommentBox] = useState(false);
  const [reply, setReply] = useState("");
  const [showReplies, setShowReplies] = useState(false);

  const handleSubmit = (event) => {
    event.preventDefault();
    //TODO: Implement logic for submitting comment reply
  };

  const handleUpvote = (event) => {
    //TODO: Implement logic for upvoting comment
  };

  const handleDownvote = (event) => {
    //TODO: Implement logic for downvoting comment
  };

  return (
    <div className="comment">
      <div className="comment-left">
        <div className="comment-user">{props.userName}</div>
        <div className="comment-text">{props.text}</div>
        <div className="comment-actions">
          <span onClick={handleUpvote}>Upvote</span>
          <span onClick={handleDownvote}>Downvote</span>
          <span onClick={() => setShowCommentBox(!showCommentBox)}>
            Reply
          </span>
        </div>
      </div>
      <div className="comment-right">
        <div className="comment-date">{props.date}</div>
      </div>
      {showCommentBox && (
        <div className="comment-reply">
          <form onSubmit={handleSubmit}>
            <textarea
              className="comment-reply-textarea"
              placeholder="Write a reply..."
              value={reply}
              onChange={(e) => setReply(e.target.value)}
            ></textarea>
            <button type="submit" className="comment-reply-submit">
              Submit
            </button>
          </form>
        </div>
      )}
      {props.replies.length > 0 && (
        <div className="comment-replies">
          <span onClick={() => setShowReplies(!showReplies)}>
            {showReplies ? "Hide replies" : `View ${props.replies.length} replies`}
          </span>
          {showReplies &&
            props.replies.map((reply, index) => (
              <Comment
                key={index}
                userName={reply.userName}
                text={reply.text}
                date={reply.date}
                replies={reply.replies}
              />
            ))}
        </div>
      )}
    </div>
  );
};

export default Comment;##JOB_COMPLETE##