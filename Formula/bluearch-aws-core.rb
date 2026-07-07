class BluearchAwsCore < Formula
  desc "Shared local runtime for BlueArch AWS tools"
  homepage "https://github.com/bluearchio/bluearch-aws-core"
  url "https://dist.bluearch.io/releases/bluearch-aws-core/v0.2.5/bluearch-aws-core-macos-arm64.zip"
  version "v0.2.5"
  sha256 "783493fdcd18ac0a27c06a37b96ab90cd2c35e64a027f02d26d05910b86121fd"
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
