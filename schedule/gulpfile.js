const gulp = require('gulp'),
  sass = require('gulp-sass')(require('sass')),
  cssnano     = require('gulp-cssnano'), 
	rename      = require('gulp-rename'); 

gulp.task('sass', function () { 
  return gulp.src('static/styles/scss/**/*.scss') 
    .pipe(sass())
    .pipe(cssnano())
    .pipe(rename({suffix: '.min'}))
    .pipe(gulp.dest('static/styles/css')) 
});

gulp.task('watch', function() {
	gulp.watch('static/styles/scss/**/*.scss', gulp.parallel('sass'));
});

gulp.task('default', gulp.parallel('sass', 'watch'));