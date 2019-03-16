{ pkgs ? import <nixpkgs> {} }:
with pkgs; mkShell {
    name = "Python";
    buildInputs = [ (python36.withPackages(ps: with ps;
                        [ slackclient
                          statsmodels
                          numpy
                          pytz
                          flake8
                          pytest
                        ]
                    ))
                  ];
    shellHook = ''
        . .alias
    '';
}
