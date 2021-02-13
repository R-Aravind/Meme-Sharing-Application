import React from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';

const Basic = (props) => (
   <div className="form-container">
     <h1 className="mt-10 text-xl">Submit a meme</h1>
     <Formik 
       initialValues={{ name: '', caption: '', url: '' }}
       validate={values => {

         const errors = {};
         if (!values.url) {
           errors.url = 'Please enter meme image url';
         } else if (
           !/(http(s?):)([/|.|\w|\s|-])*\.(?:jpg|gif|png)/i.test(values.url)
         ) {
           errors.url = 'Invalid URL';
         }
         if (!values.name) {
          errors.name = 'Please enter your username.';
        }
        if (!values.caption) {
          errors.caption = 'Please enter meme caption.';
        }
         return errors;

       }}
       onSubmit={(values, { setSubmitting }) => {
         setTimeout(() => {
           props.postMemes(values);
           setSubmitting(false);
         }, 400);
       }}
     >
       {({ isSubmitting }) => (
         <Form className="form">
            <label className="" htmlFor="form-name">Username: </label>
            <Field type="text" id="form-name" name="name" className="form-input"/>
            <ErrorMessage name="name" component="div" class="form-error" />

            <label className="mt-5" htmlFor="form-caption">Caption: </label>
            <Field type="text" id="form-caption" name="caption" className="form-input"/>
            <ErrorMessage name="caption" component="div" class="form-error" />

            <label className="mt-5" htmlFor="form-url">Meme URL: </label>
            <Field type="text" id="form-url" name="url" className="form-input"/>
            <ErrorMessage name="url" component="div" class="form-error" />
           
            <button type="submit" disabled={isSubmitting} className="form-button">
              Submit
            </button>
         </Form>
       )}
       
     </Formik>
   </div>
 );
 
 export default Basic;