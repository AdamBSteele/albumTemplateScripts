albumTemplateScripts
====================

Takes jAlbum files and turns them into static html.

Currently supports the following <ja> tags:

\<ja: if exists{$VAR}>
\<ja: if test={$VAR}>

Also supports replacement of \${VARS} inside of attributes or text.

Currently, we are working on find the source of more variables, especially those related to path.
We are alsow working on more complex \<ja> tags such as complex "if" statements.
