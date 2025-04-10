<script setup>

defineProps({
    loading: Boolean
});
</script>

<template>
    <v-overlay :model-value="loading" class="d-flex justify-center align-center">
        <div class="pl">
            <div class="pl__dot"></div>
            <div class="pl__dot"></div>
            <div class="pl__dot"></div>
            <div class="pl__dot"></div>
            <div class="pl__dot"></div>
            <div class="pl__dot"></div>
            <div class="pl__dot"></div>
            <div class="pl__dot"></div>
            <div class="pl__dot"></div>
            <div class="pl__dot"></div>
            <div class="pl__dot"></div>
            <div class="pl__dot"></div>
            <div class="pl__text">Загрузка...</div>
        </div>
    </v-overlay>
</template>

<style scoped lang="sass">
*
    border: 0
    box-sizing: border-box
    margin: 0
    padding: 0
$hue: 223
\:root
    --trans-dur: 0.3s
    font-size: calc(16px + (20 - 16) * (100vw - 320px) / (1280 - 320))

body
    background:
        color: #454954
        image: linear-gradient(135deg, hsla(0, 0%, 0%, 0), hsla(0, 0%, 0%, 0.2))
    color: #e3e4e8
    font: 1em/1.5 "Varela Round", Helvetica, sans-serif
    height: 100vh
    min-height: 360px
    display: grid
    place-items: center
    transition: background-color var(--trans-dur), color var(--trans-dur)

.pl
    box-shadow: 2em 0 2em hsla(0, 0%, 0%, 0.2) inset, -2em 0 2em hsla(0, 0%, 100%, 0.1) inset
    display: flex
    justify-content: center
    align-items: center
    position: relative
    letter-spacing: 0.1em
    text-transform: uppercase
    transform: rotateX(30deg) rotateZ(45deg)
    width: 15em
    height: 15em

    &,
    &__dot
        border-radius: 50%

    &__dot
        $dur: 2s
        animation-name: shadow
        box-shadow: 0.1em 0.1em 0 0.1em hsl(0, 0%, 0%), 0.3em 0 0.3em hsla(0, 0%, 0%, 0.5)
        top: calc(50% - 0.75em)
        left: calc(50% - 0.75em)
        width: 1.5em
        height: 1.5em

        &,
        &:before,
        &:after
            animation-duration: $dur
            animation-iteration-count: infinite
            position: absolute

        &:before,
        &:after
            content: ""
            display: block
            left: 0
            width: inherit
            transition: background-color var(--trans-dur)

        &:before
            animation-name: pushInOut1
            background-color: #454954
            border-radius: inherit
            box-shadow: 0.05em 0 0.1em hsla(0, 0%, 100%, 0.2) inset
            height: inherit
            z-index: 1

        &:after
            animation-name: pushInOut2
            background-color: #255ff4
            border-radius: 0.75em
            box-shadow: 0.1em 0.3em 0.2em hsla(0, 0%, 100%, 0.4) inset, 0 (-0.4em) 0.2em #{hsl($hue,10%,20%)} inset, 0 (-1em) 0.25em hsla(0, 0%, 0%, 0.3) inset
            bottom: 0
            clip-path: polygon(0 75%, 100% 75%, 100% 100%, 0 100%)
            height: 3em
            transform: rotate(-45deg)
            transform-origin: 50% 2.25em
        $dots: 12
        $zIndices: (5, 4, 3, 2, 1, 1, 2, 3, 4, 5, 6, 6)
        @for $i from 1 through $dots
            &:nth-child(#{$i})
                $angle: calc(360deg / $dots * ($i - 1))
                transform: rotate(-$angle) translateX(5em) rotate($angle)
                z-index: nth($zIndices, $i)

                &,
                &:before,
                &:after
                    animation-delay: $dur * (-($i - 1) / $dots)

    &__text
        font-size: 0.75em
        max-width: 5rem
        position: relative
        text-shadow: 0 0 0.1em rgba(227, 228, 232, 0.5)
        color: white
        transform: rotateZ(-45deg)

@keyframes shadow
    from
        animation-timing-function: ease-in
        box-shadow: 0.1em 0.1em 0 0.1em hsl(0, 0%, 0%), 0.3em 0 0.3em hsla(0, 0%, 0%, 0.3)
    25%
        animation-timing-function: ease-out
        box-shadow: 0.1em 0.1em 0 0.1em hsl(0, 0%, 0%), 0.8em 0 0.8em hsla(0, 0%, 0%, 0.5)
    50%,
    to
        box-shadow: 0.1em 0.1em 0 0.1em hsl(0, 0%, 0%), 0.3em 0 0.3em hsla(0, 0%, 0%, 0.3)

@keyframes pushInOut1
    from
        animation-timing-function: ease-in
        background-color: #454954
        transform: translate(0, 0)
    25%
        animation-timing-function: ease-out
        background-color: #5583f6
        transform: translate(-71%, -71%)
    50%,
    to
        background-color: #454954
        transform: translate(0, 0)

@keyframes pushInOut2
    from
        animation-timing-function: ease-in
        background-color: #454954
        clip-path: polygon(0 75%, 100% 75%, 100% 100%, 0 100%)
    25%
        animation-timing-function: ease-out
        background-color: #255ff4
        clip-path: polygon(0 25%, 100% 25%, 100% 100%, 0 100%)
    50%,
    to
        background-color: #454954
        clip-path: polygon(0 75%, 100% 75%, 100% 100%, 0 100%)
</style>