import React from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';
 
const EditMemeForm = (props) => (
     <Formik 
       initialValues={{ name: props.name, caption: props.caption, url: props.url, id: props.id}}
       validate={values => {

        const errors = {};
        if (!values.url) {
            errors.url = 'URL is required.';
          } else if (
            !/(http(s?):)([/|.|\w|\s|-])*\.(?:jpg|gif|png)/i.test(values.url)
          ) {
            errors.url = 'Invalid URL';
          }
          if (!values.name) {
           errors.name = 'Please enter your username.';
         }
         if (!values.caption) {
           errors.caption = 'Caption is required';
         }
          return errors;
 
        }}

       onSubmit={(values, { setSubmitting }) => {
         setTimeout(() => {
            props.updateMeme(values)
           setSubmitting(false);
         }, 400);
       }}
     >
       {({ isSubmitting }) => (
         <Form className="w-full mt-5">
            <Field type="text" name="name" className="bg-gray-100 card-input" placeholder="Please enter meme caption" disabled="true"/>

           <Field type="text" name="caption" className="card-input" placeholder="Please enter meme caption"/>
           <ErrorMessage name="caption" component="div" class="form-error" />

           <Field type="text" name="url" className="card-input" placeholder="Please enter meme url"/>
           <ErrorMessage name="url" component="div" class="form-error" />

           <button type="submit" disabled={isSubmitting} className="card-comment-button">
             Update
           </button>
         </Form>
       )}
       
     </Formik>
 );
 
 export default EditMemeForm;