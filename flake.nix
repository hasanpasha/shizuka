{
  description = "Application packaged using poetry2nix";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.11";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, flake-utils, poetry2nix }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {inherit system;};
        inherit (poetry2nix.lib.mkPoetry2Nix { inherit pkgs; }) 
          mkPoetryApplication 
          defaultPoetryOverrides;
      in
      {
        packages = {
          shizuka = mkPoetryApplication { 
            projectDir = self;
            python = pkgs.python39;
            overrides = defaultPoetryOverrides.extend
              (self: super: {
                pyinquirer = super.pyinquirer.overridePythonAttrs
                (
                  old: {
                    buildInputs = (old.buildInputs or [ ]) ++ [ super.setuptools ];
                  }
                );
              });
          };
          default = self.packages.${system}.shizuka;
        };

        devShells.default = pkgs.mkShell {
          inputsFrom = [ self.packages.${system}.shizuka ];
          packages = [ pkgs.poetry ];
        };
      });
}
