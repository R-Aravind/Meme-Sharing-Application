// Libraries
import React from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';
 
const CommentForm = (props) => (
     <Formik 
       initialValues={{ name: '', content: '', meme_id: props.id}}
       validate={values => {

        const errors = {};
        if (!values.name) {
          errors.name = 'Please enter your username.';
        }
        if (!values.content) {
          errors.content = 'Please enter your comment.';
        }
        return errors;

      }}
       onSubmit={(values, { setSubmitting }) => {
         setTimeout(() => {
            props.postComment(values)
           setSubmitting(false);
         }, 400);
       }}
     >
       {({ isSubmitting }) => (
         <Form className="w-full mt-5">
           <Field type="text" name="name" className="card-input" placeholder="Username"/>
           <ErrorMessage name="name" component="div" class="form-error" />

           <Field type="text" name="content" className="card-input" placeholder="Post a comment"/>
           
           <button type="submit" disabled={isSubmitting} className="card-comment-button">
             Post
           </button>
         </Form>
       )}
       
     </Formik>
 );
 
 export default CommentForm;