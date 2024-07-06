#
# ~/.zshrc
#

source ~/.rev

if [ -z "${WAYLAND_DISPLAY}" ];
then #X11-specific shit
  echo "X11 doesn't have its own .rev" >&2
else #wayland-specific shit
  source ~/.rev_wayland
fi
printf "Welcome to zsh!" >&2

# BEGIN_KITTY_SHELL_INTEGRATION
if test -n "$KITTY_INSTALLATION_DIR" -a -e "$KITTY_INSTALLATION_DIR/shell-integration/zsh/kitty.zsh"; then
  source "$KITTY_INSTALLATION_DIR/shell-integration/zsh/kitty.zsh"
fi
# END_KITTY_SHELL_INTEGRATION

# The following lines were added by compinstall

zstyle ':completion:*' auto-description '[%d]'
zstyle ':completion:*' completer _expand _complete _ignored _match _correct _approximate _prefix
zstyle ':completion:*' expand prefix suffix
zstyle ':completion:*' format $' → \033[4m%d\033[0m\n'
zstyle ':completion:*' group-name ''
zstyle ':completion:*' list-colors ''
zstyle ':completion:*' list-prompt '%SAt %p: Hit TAB for more, or the character to insert%s'
zstyle ':completion:*' matcher-list ''
zstyle ':completion:*' max-errors 2
zstyle ':completion:*' menu select=1
zstyle ':completion:*' original true
zstyle ':completion:*' preserve-prefix '//[^/]##/'
zstyle ':completion:*' prompt 'Whoops!\n'
zstyle ':completion:*' select-prompt '%SScrolling active: current selection at %p%s'
zstyle ':completion:*' squeeze-slashes true
zstyle ':completion:*' verbose true
zstyle :compinstall filename '/home/riedler/.zshrc'

autoload -Uz compinit
compinit
# End of lines added by compinstall

# custom prompt
setopt PROMPT_SUBST
function prompt_git_branch() {
    local branch merger

    branch=$(git branch 2>/dev/null | sed -n -e 's/^\* //p')
    if [[ "${branch}" != '' ]]; then
        printf "\033[2m[\033[0m" # grey opening bracket

        # check if currently in a merge operation
        if [[ -f ".git/MERGE_HEAD" ]]; then
            merger=$(git describe --exact-match --all MERGE_HEAD 2>&1)
            if [[ "${merger}" != '' ]]; then
                printf "\033[34mmerging \033[0m${merger}\033[34m into\033[0m "
            else
                printf "\033[34mmerging in\033[0m "
            fi
        fi

        printf "\033[32m${branch}\033[0m\033[2m]\033[0m"
    fi
}
PROMPT=$'%{\n%(0?..(%F{red}%?%f%) )$(prompt_git_branch)\r\033[1A%}%{\e[0m\e[34m%}%m%{\e[33m%}%~%{\e[39m%}%(!.#.\$) '

# history stuff
setopt hist_ignore_all_dups # no duplicates in history
setopt APPEND_HISTORY # append to history file after exit
SAVEHIST=10000
HISTSIZE=10000
HISTFILE=~/.zsh_history

# no BEL on complete
unsetopt beep

# define word chars to un-define this insane default >:(
WORDCHARS=""

# keybinds
bindkey -e
bindkey "^[[H"      beginning-of-line   # Pos1/Home
bindkey "^[[F"      end-of-line         # End
bindkey "^[[3~"     delete-char         # Del
bindkey "^[[3;5~"   delete-word         # Ctrl+Del
bindkey "^[[1;5D"   backward-word       # Ctrl+Left
bindkey "^[[1;5C"   forward-word        # Ctrl+Right

# custom Autocompletions
compdef girl=man
compdef _gnu_generic lmms
compdef _gnu_generic lmms-git

# "command not found" handler
# modified code from: https://wiki.archlinux.org/title/Zsh#pacman_-F_%22command_not_found%22_handler
function command_not_found_handler {
    printf 'zsh: command not found: %s\n…looking for packages…' "$1"
    local entries=(
        ${(f)"$(/usr/bin/pacman -F --machinereadable -- "$1")"}
    )
    printf '\033[2K\r' # clear loading message regardless of if something was found or not
    if (( ${#entries[@]} ))
    then
        #printf "$1 may be found in the following packages:\n"
        local pkg
        for entry in "${entries[@]}"
        do
            # (repo package version file)
            local fields=(
                ${(0)entry}
            )
            # check if /bin/ in path
            if [[ "${fields[4]}" =~ ".*/bin/.*" ]]; then
                ;
            else
                continue
            fi
            # check if package is installed
            if pacman -Qq "${fields[2]}" >/dev/null 2>/dev/null; then
                continue
            fi
            if [[ "$pkg" != "${fields[2]}" ]]; then
                printf "\033[36m%s/\033[4m%s\033[0m \033[32m%s\033[0m" "${fields[1]}" "${fields[2]}" "${fields[3]}"
            fi
            printf "\033[%sG\033[2m/%s\033[0m\n" $((${#fields[1]}+${#fields[2]}+${#fields[3]}+4)) "${fields[4]}"
            pkg="${fields[2]}"
        done
    fi
    return 127
}

printf "\n"
