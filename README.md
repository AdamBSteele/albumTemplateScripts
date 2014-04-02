albumTemplateScripts
====================

Takes jAlbum files and turns them into static html.


Step 1)  Parse input files and build dictionary of variables.

Step 2)  Use variables to resolve \<ja> tags and htt variables.

Currently supports the following <ja> tags:

\<ja: if exists{$VAR}>
\<ja: if test={$VAR}>

Also supports replacement of ${VARS} inside of attributes or text.

Currently, we are working on finding the source of more variables, especially those related to path.We are alsow working on more complex  tags such as complex "if" statements.
