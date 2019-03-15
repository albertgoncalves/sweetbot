{ pkgs ? import <nixpkgs> {} }:
with pkgs; mkShell {
    name = "Python";
    buildInputs = [ (python36.withPackages(ps: with ps;
                        [ slackclient
                          statsmodels
                          numpy
                          flake8
                          pytest
                        ]
                    ))
                  ];
    shellHook = ''
        if [ $(uname -s) = "Darwin" ]; then
            alias ls='ls --color=auto'
            alias ll='ls -al'
        fi

        alias flake8="flake8 --ignore E124,E128,E201,E203,E241,E402,W503,E722"
        alias python="env $(cat .env | xargs) python"
    '';
}
