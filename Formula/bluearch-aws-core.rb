class BluearchAwsCore < Formula
  desc "Shared local runtime for BlueArch AWS tools"
  homepage "https://github.com/bluearchio/bluearch-aws-core"
  url "https://dist.bluearch.io/releases/bluearch-aws-core/v0.2.5/bluearch-core-macos-arm64.zip"
  version "v0.2.5"
  sha256 "11ef61cf85fbea2f858210e5eeb832bc831ab3d7a1f3ba53e008dc999ad3be3a"
  license "MIT"

  depends_on arch: :arm64

  def install
    bin.install "bluearch-core"
  end

  def caveats
    <<~EOS
      bluearch-aws-core has been installed.

      Start the shared runtime and installed web dashboards:
        bluearch-core start --daemon

      API docs:
        http://127.0.0.1:8094/docs
    EOS
  end

  test do
    system "#{bin}/bluearch-core", "--version"
  end
end
