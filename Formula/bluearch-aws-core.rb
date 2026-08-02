class BluearchAwsCore < Formula
  desc "Shared local runtime for BlueArch AWS tools"
  homepage "https://github.com/bluearchio/bluearch-aws-core"
  url "https://github.com/bluearchio/bluearch-aws-core/releases/download/v0.2.8/bluearch-aws-core-macos-arm64.zip"
  version "0.2.8"
  sha256 "3b997ba0d314c1a711a06cf3c864756646be6292edb6d44837e76cbebedc509b"
  license "MIT"

  depends_on arch: :arm64

  def install
    bin.install "bluearch-aws-core"
  end

  def caveats
    <<~EOS
      bluearch-aws-core has been installed.

      Commands:
        bluearch-aws-core --help

      Start the shared runtime before using the other BlueArch AWS tools:
        bluearch-aws-core start --daemon

      API docs:
        http://127.0.0.1:8094/docs
    EOS
  end

  test do
    system "#{bin}/bluearch-aws-core", "--version"
  end
end
