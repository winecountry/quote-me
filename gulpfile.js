const gulp = require('gulp'),
    gutil = require('gulp-util'),
    browserify = require('gulp-browserify'),
    concat = require('gulp-concat');

const jsSources = [
    'daily_quote/static/daily_quote/*.js'
];
const jsDestination = 'static/dist';

gulp.task('js', function () {
    gulp.src(jsSources)
        .pipe(concat('main.js'))
        .pipe(browserify())
        .pipe(gulp.dest(jsDestination))
});
