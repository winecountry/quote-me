const gulp = require('gulp'),
    gutil = require('gulp-util'),
    browserify = require('gulp-browserify'),
    browserSync = require('browser-sync').create(),
    compass = require('gulp-compass'),
    concat = require('gulp-concat'),
    path = require('path');

// define directories
const STATIC_ROOT = 'static';
const src = path.join(STATIC_ROOT, 'src');
const dest = path.join(STATIC_ROOT, 'dist');
const image = path.join(STATIC_ROOT, 'images');
const css = path.join(dest, 'css');
const js = path.join(dest, 'js');
const sass = path.join(src, 'sass');

// master sass files
const sassSources = [
    path.join(sass, 'style.scss')
];

// all js scripts
const jsSources = [
    path.join(src, 'scripts', '*.js')
];

// compile sass
gulp.task('compass', function () {
    gulp.src(sassSources)
        .pipe(compass({
            css: css,
            sass: sass,
            image: image,
            style: 'expanded'
        }))
        .pipe(gulp.dest(css))
        .pipe(browserSync.stream());
});

// concatenate all js sources
gulp.task('js', function () {
    gulp.src(jsSources)
        .pipe(concat('script.js'))
        .pipe(browserify())
        .pipe(gulp.dest(js));
});

// ensure 'js' task is complete before browser reload
gulp.task('js-watch', ['js'], function (done) {
    browserSync.reload();
    done();
});

gulp.task('default', ['js'], function () {
    browserSync.init({
        proxy: "localhost:8000"
    });

    // reload page after html changes
    gulp.watch(path.join('templates', '**/*.html')).on('change', browserSync.reload);

    // inject css after sass changes
    gulp.watch(path.join(sass, '*.scss'), ['compass']);

    // reload after js changes
    gulp.watch(path.join(js, '*.js'), ['js-watch']);
});
