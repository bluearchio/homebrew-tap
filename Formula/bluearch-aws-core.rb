class BluearchAwsCore < Formula
  desc "Shared local runtime for BlueArch AWS tools"
  homepage "https://github.com/bluearchio/bluearch-aws-core"
  url "https://dist.bluearch.io/releases/bluearch-aws-core/v0.2.5/bluearch-core-macos-arm64.zip"
  version "v0.2.5"
  sha256 "11ef61cf85fbea2f858210e5eeb832bc831ab3d7a1f3ba53e008dc999ad3be3a"
  license "MIT"

  depends_on arch: :arm64
  conflicts_with "bluearch-core", because: "bluearch-core was the old private formula name"

  def install
    bin.install "bluearch-core"
    alias_path = bin/"bluearch-aws-core"
    alias_path.write <<~SH
      #!/bin/sh
      exec "#{bin}/bluearch-core" "$@"
    SH
    alias_path.chmod 0755
  end

  def caveats
    <<~EOS
      bluearch-aws-core has been installed.

      Commands:
        bluearch-aws-core --help
        bluearch-core --help

      Start the shared runtime before using the other BlueArch AWS tools:
        bluearch-aws-core start --daemon

      API docs:
        http://127.0.0.1:8094/docs
    EOS
  end

  test do
    system "#{bin}/bluearch-aws-core", "--version"
    system "#{bin}/bluearch-core", "--version"
  end
end
