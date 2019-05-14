{ pkgs ? import <nixpkgs> {} }:
with pkgs; mkShell {
    name = "Python";
    buildInputs = [
        (python37.withPackages(ps: with ps; [
            slackclient
            statsmodels
            numpy
            pytz
            pytest
            mypy
            flake8
        ]))
    ];
    shellHook = ''
        . .shellhook
    '';
}
